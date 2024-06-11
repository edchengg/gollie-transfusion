from typing import Any, Dict, List, Type, Union

from typing_extensions import override
import collections
from .utils_typing import Entity, Event, Relation, Template, Value
import json
import math
import re
import string

class Scorer:
    """An abstract class for scorers."""

    def __call__(self, reference: List[Any], predictions: List[Any]) -> Dict[str, Dict[str, float]]:
        """
        Computes the scores for the given reference and predictions.

        Args:
            reference (`List[Any]`):
                The list of reference or gold annotations.
            predictions (`List[Any]`):
                The list of predicted annotations.

        Returns:
            Dict[str, Dict[str, float]]:
                A `dict` object that contains the scores (usually Precision, Recall and
                F1-score) for the evaluated tasks.
        """
        raise NotImplementedError("This method must be implemented.")

    def _filter_valid_types(self, elems: List[Any]) -> List[Any]:
        """
        Filters the non-valid annotations for a given task.

        Args:
            elems (`List[Any]`):
                List of annotations to filter based on the predefined valid types.

        Returns:
            `List[Union[Entity, Value]]`:
                List of the filtered annotations to keep only the ones defined by the
                valid types.
        """
        return [elem for elem in elems if any(isinstance(elem, _type) for _type in self.valid_types)]


class SpanScorer(Scorer):
    """A general scorer implementation for span identification and classification
    tasks.
    """

    valid_types: List[Type] = [Entity, Value]

    @override
    def __call__(
        self,
        reference: List[Union[Entity, Value]],
        predictions: List[Union[Entity, Value]],
    ) -> Dict[str, Dict[str, float]]:
        if not len(reference) or (len(reference) and not isinstance(reference[0], list)):
            reference = [reference]
        if not len(predictions) or (len(predictions) and not isinstance(predictions[0], list)):
            predictions = [predictions]

        assert len(reference) == len(
            predictions
        ), f"Reference ({len(reference)}) and prediction ({len(predictions)}) amount must be equal."

        tp = total_pos = total_pre = 0

        class_scores = {}

        for ref, pre in zip(reference, predictions):
            
            # ref = self._filter_valid_types(ref)
            # pre = self._filter_valid_types(pre)
            
            ref2 = ref.copy()
            pre2 = pre.copy()

            total_pos += len(ref)
            total_pre += len(pre)
            for entity in pre:
                if entity in ref:
                    tp += 1
                    ref.pop(ref.index(entity))

            # Calculate class scores
            for entity in ref2:
                label = type(entity).__name__
                if label not in class_scores:
                    class_scores[label] = {"tp": 0, "total_pos": 0, "total_pre": 0}
                class_scores[label]["total_pos"] += 1

            for entity in pre2:
                label = type(entity).__name__
                if label not in class_scores:
                    class_scores[label] = {"tp": 0, "total_pos": 0, "total_pre": 0}
                class_scores[label]["total_pre"] += 1
                if entity in ref2:
                    class_scores[label]["tp"] += 1
                    ref2.pop(ref2.index(entity))

        precision = tp / total_pre if total_pre > 0.0 else 0.0
        recall = tp / total_pos if total_pos > 0.0 else 0.0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0.0 else 0.0
        # Calculate class scores
        for label in class_scores:
            class_scores[label]["precision"] = (
                class_scores[label]["tp"] / class_scores[label]["total_pre"]
                if class_scores[label]["total_pre"] > 0.0
                else 0.0
            )
            class_scores[label]["recall"] = (
                class_scores[label]["tp"] / class_scores[label]["total_pos"]
                if class_scores[label]["total_pos"] > 0.0
                else 0.0
            )
            class_scores[label]["f1-score"] = (
                2
                * class_scores[label]["precision"]
                * class_scores[label]["recall"]
                / (class_scores[label]["precision"] + class_scores[label]["recall"])
                if (class_scores[label]["precision"] + class_scores[label]["recall"]) > 0.0
                else 0.0
            )

        return {
            "spans": {"precision": precision, "recall": recall, "f1-score": f1_score, "class_scores": class_scores},
        }


class QAScorer(Scorer):
    """A QA scorer implementation for question answering task.
    """

    valid_types: List[Type] = [Entity]

    @override
    def __call__(
        self,
        reference: List[Union[Entity]],
        predictions: List[Union[Entity]],
    ) -> Dict[str, Dict[str, float]]:
        if not len(reference) or (len(reference) and not isinstance(reference[0], list)):
            reference = [reference]
        if not len(predictions) or (len(predictions) and not isinstance(predictions[0], list)):
            predictions = [predictions]

        assert len(reference) == len(
            predictions
        ), f"Reference ({len(reference)}) and prediction ({len(predictions)}) amount must be equal."

        def normalize_answer(s):
            """Lower text and remove punctuation, articles and extra whitespace."""

            def remove_articles(text):
                regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
                return re.sub(regex, " ", text)

            def white_space_fix(text):
                return " ".join(text.split())

            def remove_punc(text):
                exclude = set(string.punctuation)
                return "".join(ch for ch in text if ch not in exclude)

            def lower(text):
                return text.lower()

            return white_space_fix(remove_articles(remove_punc(lower(s))))

        def get_tokens(s):
            if not s:
                return []
            return normalize_answer(s).split()

        def compute_exact(a_gold, a_pred):
            return int(normalize_answer(a_gold) == normalize_answer(a_pred))


        def compute_f1(a_gold, a_pred):
            gold_toks = get_tokens(a_gold)
            pred_toks = get_tokens(a_pred)
            common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
            num_same = sum(common.values())
            if len(gold_toks) == 0 or len(pred_toks) == 0:
                # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
                return int(gold_toks == pred_toks)
            if num_same == 0:
                return 0
            precision = 1.0 * num_same / len(pred_toks)
            recall = 1.0 * num_same / len(gold_toks)
            f1 = (2 * precision * recall) / (precision + recall)
            return f1


        def get_eval_scores(answers, preds):
            """
            Computes the exact and f1 scores from the examples and the model predictions
            https://github.com/huggingface/transformers/blob/main/src/transformers/data/metrics/squad_metrics.py#L37
            """
            exact_scores = {}
            f1_scores = {}

            for qas_id, (gold_answers, prediction) in enumerate(zip(answers, preds)):
                exact_scores[qas_id] = max(compute_exact(a, prediction) for a in gold_answers)
                f1_scores[qas_id] = max(compute_f1(a, prediction) for a in gold_answers)
            total = len(exact_scores)
            return {"qa": 
                        {
                            "exact": sum(exact_scores.values()) / total,
                            "f1": sum(f1_scores.values()) / total,
                            "total": total,
                        }     
                    }
        answers = []
        preds = []

        for refs, preds_item in zip(reference, predictions):
            # convert to text
            answer_cache = [ref.span for ref in refs]
            pred_cache = preds_item[0].span if preds_item else ""

            answers.append(answer_cache)
            preds.append(pred_cache)

        final_results = get_eval_scores(answers, preds)
        
        return final_results


class RelationScorer(SpanScorer):
    """A general scorer implementation for relation identification and
    classification tasks
    """

    valid_types: List[Type] = [Relation]

    @override
    def __call__(self, reference: List[Relation], predictions: List[Relation]) -> Dict[str, Dict[str, float]]:
        output = super().__call__(reference, predictions)
        return {"relations": output["spans"]}


class EventScorer(Scorer):
    """A general scorer implementation for event and argument extraction."""

    valid_types: List[Type] = [Event]

    @override
    def __call__(self, reference: Any, predictions: Any) -> Dict[str, Dict[str, float]]:
        if not len(reference) or (len(reference) and not isinstance(reference[0], list)):
            reference = [reference]
        if not len(predictions) or (len(predictions) and not isinstance(predictions[0], list)):
            predictions = [predictions]

        assert len(reference) == len(
            predictions
        ), f"Reference ({len(reference)}) and prediction ({len(predictions)}) amount must be equal."
        e_tp = e_total_pos = e_total_pre = 0
        a_tp = a_total_pos = a_total_pre = 0

        event_scores = {}

        for ref, pre in zip(reference, predictions):
            # ref = self._filter_valid_types(ref)
            # pre = self._filter_valid_types(pre)
            ref2 = ref.copy()
            pre2 = pre.copy()

            e_total_pos += len(ref)
            for event in ref:
                a_total_pos += len(event)

            e_total_pre += len(pre)
            for pre_event in pre:
                a_total_pre += len(pre_event)
                if pre_event in ref:
                    ref_event = ref.pop(ref.index(pre_event))
                    e_tp += 1
                    a_tp += len(ref_event & pre_event)

            # Calculate argument scores
            for event in ref2:
                label = type(event).__name__
                if label not in event_scores:
                    event_scores[label] = {"tp": 0, "total_pos": 0, "total_pre": 0}
                event_scores[label]["total_pos"] += 1

            for event in pre2:
                label = type(event).__name__
                if label not in event_scores:
                    event_scores[label] = {"tp": 0, "total_pos": 0, "total_pre": 0}
                event_scores[label]["total_pre"] += 1
                if event in ref2:
                    event_scores[label]["tp"] += 1
                    ref2.pop(ref2.index(event))

        e_precision = e_tp / e_total_pre if e_total_pre > 0.0 else 0.0
        a_precision = a_tp / a_total_pre if a_total_pre > 0.0 else 0.0
        e_recall = e_tp / e_total_pos if e_total_pos > 0.0 else 0.0
        a_recall = a_tp / a_total_pos if a_total_pos > 0.0 else 0.0
        e_f1_score = 2 * e_precision * e_recall / (e_precision + e_recall) if (e_precision + e_recall) > 0.0 else 0.0
        a_f1_score = 2 * a_precision * a_recall / (a_precision + a_recall) if (a_precision + a_recall) > 0.0 else 0.0

        # Calculate event scores
        for label in event_scores:
            event_scores[label]["precision"] = (
                event_scores[label]["tp"] / event_scores[label]["total_pre"]
                if event_scores[label]["total_pre"] > 0.0
                else 0.0
            )
            event_scores[label]["recall"] = (
                event_scores[label]["tp"] / event_scores[label]["total_pos"]
                if event_scores[label]["total_pos"] > 0.0
                else 0.0
            )
            event_scores[label]["f1-score"] = (
                2
                * event_scores[label]["precision"]
                * event_scores[label]["recall"]
                / (event_scores[label]["precision"] + event_scores[label]["recall"])
                if (event_scores[label]["precision"] + event_scores[label]["recall"]) > 0.0
                else 0.0
            )

        return {
            "events": {
                "precision": e_precision,
                "recall": e_recall,
                "f1-score": e_f1_score,
                "class_scores": event_scores,
            },
            "arguments": {
                "precision": a_precision,
                "recall": a_recall,
                "f1-score": a_f1_score,
            },
        }


class TemplateScorer(Scorer):
    """A general scorer implementation for template extraction."""

    valid_types: List[Type] = [Template]

    @override
    def __call__(self, reference: Any, predictions: Any) -> Dict[str, Dict[str, float]]:
        if not len(reference) or (len(reference) and not isinstance(reference[0], list)):
            reference = [reference]
        if not len(predictions) or (len(predictions) and not isinstance(predictions[0], list)):
            predictions = [predictions]

        assert len(reference) == len(
            predictions
        ), f"Reference ({len(reference)}) and prediction ({len(predictions)}) amount must be equal."
        t_tp = t_total_pos = t_total_pre = 0
        s_tp = s_total_pos = s_total_pre = 0

        template_scores = {}

        for ref, pre in zip(reference, predictions):
            # ref = self._filter_valid_types(ref)
            # pre = self._filter_valid_types(pre)
            ref2 = ref.copy()
            pre2 = pre.copy()

            t_total_pos += len(ref)
            for template in ref:
                s_total_pos += len(template)

            t_total_pre += len(pre)
            for pre_temp in pre:
                s_total_pre += len(pre_temp)
                if pre_temp in ref:
                    ref_temp = ref.pop(ref.index(pre_temp))
                    t_tp += 1
                    s_tp += len(ref_temp & pre_temp)

            # Calculate slot scores
            for template in ref2:
                label = type(template).__name__
                if label not in template_scores:
                    template_scores[label] = {"tp": 0, "total_pos": 0, "total_pre": 0}
                template_scores[label]["total_pos"] += 1

            for template in pre2:
                label = type(template).__name__
                if label not in template_scores:
                    template_scores[label] = {"tp": 0, "total_pos": 0, "total_pre": 0}
                template_scores[label]["total_pre"] += 1
                if template in ref2:
                    template_scores[label]["tp"] += 1
                    ref2.pop(ref2.index(template))

        t_precision = t_tp / t_total_pre if t_total_pre > 0.0 else 0.0
        s_precision = s_tp / s_total_pre if s_total_pre > 0.0 else 0.0
        t_recall = t_tp / t_total_pos if t_total_pos > 0.0 else 0.0
        s_recall = s_tp / s_total_pos if s_total_pos > 0.0 else 0.0
        t_f1_score = 2 * t_precision * t_recall / (t_precision + t_recall) if (t_precision + t_recall) > 0.0 else 0.0
        s_f1_score = 2 * s_precision * s_recall / (s_precision + s_recall) if (s_precision + s_recall) > 0.0 else 0.0

        # Calculate template scores
        for label in template_scores:
            template_scores[label]["precision"] = (
                template_scores[label]["tp"] / template_scores[label]["total_pre"]
                if template_scores[label]["total_pre"] > 0.0
                else 0.0
            )
            template_scores[label]["recall"] = (
                template_scores[label]["tp"] / template_scores[label]["total_pos"]
                if template_scores[label]["total_pos"] > 0.0
                else 0.0
            )
            template_scores[label]["f1-score"] = (
                2
                * template_scores[label]["precision"]
                * template_scores[label]["recall"]
                / (template_scores[label]["precision"] + template_scores[label]["recall"])
                if (template_scores[label]["precision"] + template_scores[label]["recall"]) > 0.0
                else 0.0
            )

        return {
            "templates": {
                "precision": t_precision,
                "recall": t_recall,
                "f1-score": t_f1_score,
                "class_scores": template_scores,
            },
            "slots": {
                "precision": s_precision,
                "recall": s_recall,
                "f1-score": s_f1_score,
            },
        }
