import inspect
import json
from typing import Tuple, Union

from src.tasks.conll04.guidelines import GUIDELINES
from src.tasks.conll04.guidelines_gold import EXAMPLES
from src.tasks.conll04.prompts import (
    Person,
    Location,
    Other,
    Organization,
    OrgBasedInRelation,
    LocatedInRelation,
    KillRelation,
    LiveInRelation,
    WorkForRelation,
    ENTITY_DEFINITIONS,
    RELATION_DEFINITIONS,
)

from ..utils_data import DatasetLoader, Sampler
from src.tasks.conll04.easyproject_data import decode_data

class CoNLL04DatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the CoNLL04 dataset.

    Args:
        path (`str`):
            The location of the dataset directory.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    ENTITY_TO_CLASS_MAPPING = {
        "Peop": Person,
        "Loc": Location,
        "Other": Other,
        "Org": Organization,
    }

    RELATION_TO_CLASS_MAPPING = {
        "OrgBased_In": OrgBasedInRelation,
        "Located_In": LocatedInRelation,
        "Kill": KillRelation,
        "Live_In": LiveInRelation,
        "Work_For": WorkForRelation
    }
    
    def __init__(self, path: str, **kwargs) -> None:
        self.elements = {}

        with open(path, "rt") as in_f:
            data = json.load(in_f)
        
        for line in data:
            key = line["orig_id"]
            tokens = line["tokens"]
            entities = [
                self.ENTITY_TO_CLASS_MAPPING[entity["type"]](span=" ".join(tokens[entity["start"]:entity["end"]]))
                for entity in line["entities"]
                if entity["type"] in self.ENTITY_TO_CLASS_MAPPING
            ]

            relations = []
            for rel in line["relations"]:
                rel_type = rel["type"]
                head_idx = rel["head"]
                tail_idx = rel["tail"]
                relations.append(
                    self.RELATION_TO_CLASS_MAPPING[rel_type](
                        arg1=entities[head_idx].key(),
                        arg2=entities[tail_idx].key(),
                    )
                )
            self.elements[key] = {}
            self.elements[key]["text"] = " ".join(tokens)
            self.elements[key]["doc_id"] = key
            self.elements[key]["id"] = key
            self.elements[key]["entities"] = entities
            self.elements[key]["relations"] = relations
            self.elements[key]["gold"] = entities  # Is not used anyway

class CoNLL04TranslationDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the CoNLL04 dataset.

    Args:
        path (`str`):
            The location of the dataset directory.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    ENTITY_TO_CLASS_MAPPING = {
        "Peop": Person,
        "Loc": Location,
        "Other": Other,
        "Org": Organization,
    }

    RELATION_TO_CLASS_MAPPING = {
        "OrgBased_In": OrgBasedInRelation,
        "Located_In": LocatedInRelation,
        "Kill": KillRelation,
        "Live_In": LiveInRelation,
        "Work_For": WorkForRelation
    }
    
    def __init__(self, path: str, **kwargs) -> None:
        self.elements = {}

        with open(path, "r", encoding="utf-8") as in_f:
            data = [json.loads(line) for line in in_f]
        
        for d_idx, line in enumerate(data):
            output_sentence = line["output_sentence"]
            input_sentence = line["input_sentence"]
            marker2label = line["marker2label"]

            clean_sentence, entities = decode_data(input_sentence, output_sentence, marker2label)
            if (clean_sentence and entities) or (clean_sentence and entities == []):
                key2entities = {}

                labeled_entities = []
                for ent in entities:
                    key, span = ent
                    key2entities[key] = span.strip()
                    labeled_entities.append(
                        self.ENTITY_TO_CLASS_MAPPING[marker2label[key]](span=span.strip())
                    )

                relations = []
                for rel in marker2label["relations"]:
                    
                    #{"type": "Work_For", "head": 0, "tail": 1}
                    rel_type = rel["type"]
                    head = rel["head"]
                    tail = rel["tail"]
                    
                    relations.append(
                        self.RELATION_TO_CLASS_MAPPING[rel_type](
                            arg1=key2entities[str(head)],
                            arg2=key2entities[str(tail)],
                        )
                    )
            
                self.elements[d_idx] = {}
                self.elements[d_idx]["text"] = clean_sentence
                self.elements[d_idx]["doc_id"] = d_idx
                self.elements[d_idx]["id"] = d_idx
                self.elements[d_idx]["entities"] = labeled_entities
                self.elements[d_idx]["relations"] = relations
                self.elements[d_idx]["gold"] = labeled_entities  # Is not used anyway

class CoNLL04TransFusionDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the CoNLL04 dataset.

    Args:
        path (`str`):
            The location of the dataset directory.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    ENTITY_TO_CLASS_MAPPING = {
        "Peop": Person,
        "Loc": Location,
        "Other": Other,
        "Org": Organization,
    }

    RELATION_TO_CLASS_MAPPING = {
        "OrgBased_In": OrgBasedInRelation,
        "Located_In": LocatedInRelation,
        "Kill": KillRelation,
        "Live_In": LiveInRelation,
        "Work_For": WorkForRelation
    }
    
    def __init__(self, path: str, **kwargs) -> None:
        self.elements = {}

        with open(path, "r", encoding="utf-8") as in_f:
            data = [json.loads(line) for line in in_f]
        
        for d_idx, line in enumerate(data):
            output_sentence = line["output_sentence"]
            input_sentence = line["input_sentence"]
            marker2label = line["marker2label"]

            clean_sentence, entities = decode_data(input_sentence, output_sentence, marker2label)
            clean_en_sentence, en_entities = decode_data(input_sentence, input_sentence, marker2label)
            if (clean_sentence and entities and clean_en_sentence and en_entities) or (clean_sentence and entities == [] and clean_en_sentence and en_entities == []):
                key2entities = {}
                en_key2entities = {}

                labeled_entities = []
                for ent in entities:
                    key, span = ent
                    key2entities[key] = span.strip()
                    labeled_entities.append(
                        self.ENTITY_TO_CLASS_MAPPING[marker2label[key]](span=span.strip())
                    )

                labeled_en_entities = []
                for ent in en_entities:
                    key, span = ent
                    en_key2entities[key] = span.strip()
                    labeled_en_entities.append(
                        self.ENTITY_TO_CLASS_MAPPING[marker2label[key]](span=span.strip())
                    )

                relations = []
                en_relations = []
                for rel in marker2label["relations"]:
                    
                    #{"type": "Work_For", "head": 0, "tail": 1}
                    rel_type = rel["type"]
                    head = rel["head"]
                    tail = rel["tail"]
                    
                    relations.append(
                        self.RELATION_TO_CLASS_MAPPING[rel_type](
                            arg1=key2entities[str(head)],
                            arg2=key2entities[str(tail)],
                        )
                    )

                    en_relations.append(
                        self.RELATION_TO_CLASS_MAPPING[rel_type](
                            arg1=en_key2entities[str(head)],
                            arg2=en_key2entities[str(tail)],
                        )
                    )
            
                self.elements[d_idx] = {}
                self.elements[d_idx]["text"] = clean_sentence
                self.elements[d_idx]["en_text"] = clean_en_sentence
                self.elements[d_idx]["doc_id"] = d_idx
                self.elements[d_idx]["id"] = d_idx
                self.elements[d_idx]["entities"] = labeled_entities
                self.elements[d_idx]["en_entities"] = labeled_en_entities
                self.elements[d_idx]["relations"] = relations
                self.elements[d_idx]["en_relations"] = en_relations
                self.elements[d_idx]["gold"] = labeled_entities  
                self.elements[d_idx]["en_gold"] = labeled_en_entities 


class CoNLL04Sampler(Sampler):
    """
    A data `Sampler` for the CoNLL04 dataset.

    Args:
        dataset_loader (`CoNLL04DatasetLoader`):
            The dataset loader that contains the data information.
        task (`str`, optional):
            The task to sample. It must be one of the following: NER, RE.
            Defaults to `None`.
        split (`str`, optional):
            The split to sample. It must be one of the following: "train", "dev" or
            "test". Depending on the split the sampling strategy differs. Defaults to
            `"train"`.
        parallel_instances (`Union[int, Tuple[int, int]]`, optional):
            The number of sentences sampled in parallel. Options:

                * **`int`**: The amount of elements that will be sampled in parallel.
                * **`tuple`**: The range of elements that will be sampled in parallel.

            Defaults to 1.
        max_guidelines (`int`, optional):
            The number of guidelines to append to the example at the same time. If `-1`
            is given then all the guidelines are appended. Defaults to `-1`.
        guideline_dropout (`float`, optional):
            The probability to dropout a guideline definition for the given example. This
            is only applied on training. Defaults to `0.0`.
        seed (`float`, optional):
            The seed to sample the examples. Defaults to `0`.
        prompt_template (`str`, optional):
            The path to the prompt template. Defaults to `"templates/prompt.txt"`.
        ensure_positives_on_train (bool, optional):
            Whether to ensure that the guidelines of annotated examples are not removed.
            Defaults to `False`.
        dataset_name (str, optional):
            The name of the dataset. Defaults to `None`.
        scorer (`str`, optional):
           The scorer class import string. Defaults to `None`.
        sample_only_gold_guidelines (`bool`, optional):
            Whether to sample only guidelines of present annotations. Defaults to `False`.
    """

    def __init__(
        self,
        dataset_loader: CoNLL04DatasetLoader,
        task: str = None,
        split: str = "train",
        parallel_instances: Union[int, Tuple[int, int]] = 1,
        max_guidelines: int = -1,
        guideline_dropout: float = 0.0,
        seed: float = 0,
        ensure_positives_on_train: bool = False,
        dataset_name: str = None,
        scorer: str = None,
        sample_only_gold_guidelines: bool = False,
        use_transfusion: bool = False,
        **kwargs,
    ) -> None:
        assert task in [
            "NER",
            "RE",
        ], f"{task} must be either 'NER', 'RE'."

        if use_transfusion:
            task_definitions, task_target, task_template = {
                "NER": (ENTITY_DEFINITIONS, "entities", "templates/prompt_ner_tf.txt"),
                "RE": (RELATION_DEFINITIONS, "relations", "templates/prompt_re_tfv2.txt"),
            }[task]
        else:
            task_definitions, task_target, task_template = {
                "NER": (ENTITY_DEFINITIONS, "entities", "templates/prompt.txt"),
                "RE": (RELATION_DEFINITIONS, "relations", "templates/prompt_re.txt"),
            }[task]

        is_coarse_to_fine = False
        COARSE_TO_FINE = None
        FINE_TO_COARSE = None

        kwargs.pop("prompt_template")

        super().__init__(
            dataset_loader=dataset_loader,
            task=task,
            split=split,
            parallel_instances=parallel_instances,
            max_guidelines=max_guidelines,
            guideline_dropout=guideline_dropout,
            seed=seed,
            prompt_template=task_template,
            ensure_positives_on_train=ensure_positives_on_train,
            sample_only_gold_guidelines=sample_only_gold_guidelines,
            dataset_name=dataset_name,
            scorer=scorer,
            task_definitions=task_definitions,
            task_target=task_target,
            is_coarse_to_fine=is_coarse_to_fine,
            coarse_to_fine=COARSE_TO_FINE,
            fine_to_coarse=FINE_TO_COARSE,
            definitions=GUIDELINES,
            examples=EXAMPLES,
            use_transfusion=use_transfusion,
            **kwargs,
        )
