import glob
import importlib
import json
import logging
import os
import sys
from typing import Any, Dict, List, Type

from tqdm import tqdm
import copy
from src.config import DataTrainingArguments, ModelArguments
from src.tasks import task_id_to_prompts
from src.tasks.utils_typing import AnnotationList



class ResultLogger:
    """
    A class to log the results of a task.

    Args:
        task_name: The name of the task.
    """

    def __init__(self, task_name: str) -> None:
        self.task_name = task_name
        self.sentences: List[str] = []
        self.golds: List[AnnotationList] = []
        self.predictions: List[AnnotationList] = []
        self.impossible_to_parse: int = 0
        self.hallucinated_predictions: int = 0
        self.valid_predictions: int = 0
        self.total_predictions: int = 0
        self.gold_predictions: int = 0

    def add_sentence(self, sentence: str, gold_labels: AnnotationList, pred_labels: AnnotationList) -> None:
        """
        Add a sentence to the logger.

        Args:
            sentence: The sentence to label.
            gold_labels: The 'AnnotationList' gold labels.
            pred_labels: The 'AnnotationList' predicted labels.
        """
        filtered_pred_labels = pred_labels.filter_hallucinations(sentence)
        self.impossible_to_parse += 1 if filtered_pred_labels.parse_error else 0
        self.hallucinated_predictions += filtered_pred_labels.hallucinated_no
        self.valid_predictions += len(filtered_pred_labels)
        self.total_predictions += len(pred_labels)
        self.gold_predictions += len(gold_labels)

        self.sentences.append(sentence)
        self.golds.append(gold_labels)
        self.predictions.append(filtered_pred_labels)

    def compute_metrics(self, scorer: Any) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Compute the metrics for the task.

        Args:
            scorer: The scorer to use.

        Returns:
            A dictionary containing the metrics.
        """
        if len(self.sentences) == 0:
            raise ValueError(f"No sentences were added to the {self.task_name} logger, we cannot compute metrics.")
        
        golds = copy.deepcopy(self.golds)
        predictions = copy.deepcopy(self.predictions)
        scores: Dict[str, Dict[str, Dict[str, float]]] = scorer(reference=golds, predictions=predictions)
        results: Dict[str, Dict[str, Dict[str, float]]] = {
            "predictions_stats": {
                "impossible_to_parse": {
                    "total": self.impossible_to_parse,
                    "percentage%": round((self.impossible_to_parse / len(self.sentences)) * 100, 4),
                },
                "hallucinated_predictions": {
                    "total": self.hallucinated_predictions,
                    "percentage%": (
                        0.0
                        if self.total_predictions == 0
                        else round((self.hallucinated_predictions / self.total_predictions) * 100, 4)
                    ),
                },
                "total": {"predictions": self.valid_predictions, "gold": self.gold_predictions},
            },
        }
        scores.update(results)
        return scores

    def print_predictions(self, output_path: str):
        """
        Print the predictions to a file in json format. In the following format:
        {
            "sentence": {
                "golds": "gold labels",
                "predictions": "predicted labels"
            }
        }

        Args:
            output_path: The path to the output file.
        """
        if len(self.sentences) == 0:
            raise ValueError(f"No sentences were added to the {self.task_name} logger, we cannot print predictions.")
        with open(output_path, "w", encoding="utf8") as f:
            for sentence, prediction, gold in zip(self.sentences, self.predictions, self.golds):
                example = {sentence: {"golds": gold.to_string(), "predictions": prediction.to_string()}}
                
                f.write(json.dumps(example, ensure_ascii=False) + "\n")


def import_prompts(task_module: str) -> None:
    """Imports everything from a module.

    Args:
        task_module (str): the module to import everything from.
    """
    # get a handle on the module
    mdl = importlib.import_module(task_module)

    # # is there an __all__?  if so respect it
    # if "__all__" in mdl.__dict__:
    #     names = mdl.__dict__["__all__"]
    # else:
    #     # otherwise we import all names that don't begin with _
    #     names = [x for x in mdl.__dict__ if not x.startswith("_")]
    names = {x: y for x, y in mdl.__dict__.items() if not x.startswith("_")}

    # now drag them in
    globals().update(dict(names.items()))


def get_class(class_path: str) -> Type:
    components = class_path.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod


def fix_prompt_outputs(text: str) -> str:
    """Fixes some known structural bugs.

    Args:
        text (str): Bugged output.

    Returns:
        str: Corrected output.
    """

    text = text.replace(")\n ", "),\n ")
    return text


def remove_hallucinations(unlabelled_sentence: str, predictions: List[Any]) -> List[Any]:
    """Removes predictions that are not in the unlabelled sentence.
    Args:
        unlabelled_sentence (str): The unlabelled sentence.
        predictions (List[Any]): The list of predictions.
    Returns:
        List[Any]: The list of predictions that are in the unlabelled sentence.
    """
    accepted_list: List[Any] = []
    for prediction in predictions:
        if prediction.exists_in(unlabelled_sentence):
            accepted_list.append(prediction)
    return accepted_list


def evaluate(
    task_list,
    output_dir,
    gold_data_dir,
    max_example=None,
    split_word="result",
    save_prefix="",
) -> Dict[str, Dict[str, Dict[str, Dict[str, float]]]]:
    """This function evaluates the output of a model.

    Args:
        model_args (ModelArguments): Model arguments. See `ModelArguments` docs.
        data_args (DataTrainingArguments): Data arguments. See `DataTrainingArguments` docs.

    Returns:
        Dict[str, Dict[str, Dict[str, Dict[str, float]]]]: A dictionary containing the scores for each task
        present in the dataset.
    """
    predictions_dir = os.path.join(output_dir, "predictions")

    all_scores = {}

    scores_file_name = os.path.join(output_dir, f"{save_prefix}_task_scores.json")
    scores_file_name_summary = os.path.join(output_dir, f"{save_prefix}_task_scores_summary.json")
    with tqdm(total=len(task_list), desc="Evaluating") as pbar:
        for task in task_list:
            print(task)
            pbar.set_description(f"Evaluating {task}")
            gold_path = os.path.join(
                gold_data_dir,
                f"{task}.test.jsonl",
            )
            pred_path = os.path.join(predictions_dir, task) + ".predictions.jsonl"

            if not os.path.exists(gold_path):
                raise FileNotFoundError(f"File not found: '{gold_path}'")

            if not os.path.exists(pred_path):
                raise FileNotFoundError(f"File not found: '{pred_path}'")

            task_logger = ResultLogger(task)
            task_module = None
            scorer = None

            with open(gold_path, "rt", encoding="utf8") as gold_f, open(pred_path, "rt", encoding="utf8") as pred_f:
                gold_lines = [json.loads(g_line) for g_line in gold_f]
                pred_lines = [json.loads(p_line) for p_line in pred_f]
             
                if max_example:
                    gold_lines = gold_lines[:max_example]
                    pred_lines = pred_lines[:max_example]

                for gold_line, pred_line in zip(gold_lines, pred_lines):

                    if not task_module:
                        task_module = task_id_to_prompts(gold_line["task_id"])
                        import_prompts(task_module)

                    if not scorer:
                        scorer = get_class(gold_line["scorer_cls"])()

                    gold_labels: AnnotationList = AnnotationList.from_output(
                        str(gold_line["labels"]), task_module=task_module
                    )

                    pred_labels = pred_line["model_prediction"].strip().split(f"{split_word} = ")[-1]

                    try:
                        pred_labels: AnnotationList = AnnotationList.from_output(str(pred_labels), task_module=task_module)
                    except TypeError:
                        pred_labels = AnnotationList(elems=[])

                    task_logger.add_sentence(
                        sentence=gold_line["unlabelled_sentence"], gold_labels=gold_labels, pred_labels=pred_labels
                    )

            task_metrics = task_logger.compute_metrics(scorer)
            all_scores[task] = task_metrics
            # rich.print(f"{task} scores: {task_metrics}")
            task_logger.print_predictions(output_path=os.path.join(predictions_dir, f"{task}.eval_file.json"))
            pbar.update(1)

    with open(scores_file_name, "wt", encoding="utf8") as f:
        json.dump(all_scores, f, indent=4, ensure_ascii=False)

    for task, score in all_scores.items():
        for metric, value in score.items():
            if "class_scores" in value:
                value.pop("class_scores")

    with open(scores_file_name_summary, "wt", encoding="utf8") as f:
        json.dump(all_scores, f, indent=4, ensure_ascii=False)

    logging.info(
        f"Scores saved in: {scores_file_name}. A summary without class scores saved in: {scores_file_name_summary}"
    )

    return all_scores

