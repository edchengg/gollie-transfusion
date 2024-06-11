from typing import Dict, List, Tuple, Type, Union
import json
from src.tasks.uner.guidelines import GUIDELINES
from src.tasks.uner.guidelines_gold import EXAMPLES
from src.tasks.uner.prompts import (
    ENTITY_DEFINITIONS,
    ENTITY_DEFINITIONS_woMISC,
    Location,
    Miscellaneous,
    Organization,
    Person,
)
from src.tasks.label_encoding import rewrite_labels

from ..utils_data import DatasetLoader, Sampler
from ..utils_typing import Entity

def read_tsv(filepath):
    """
    READ tsv file in conll format
    Args:
        filepath: Path to the file
    Returns: List of words, List of labels
    """
    dataset_words: List[List[str]] = []
    dataset_labels: List[List[str]] = []
    with open(filepath, encoding="utf-8") as f:
        guid = 0
        tokens = []
        ner_tags = []
        for line in f:
            if line.startswith("#") or line == "" or line == "\n":
                if tokens:
                    dataset_words.append(tokens)
                    dataset_labels.append(ner_tags)

                    guid += 1
                    tokens = []
                    ner_tags = []
            else:
                # uner uses tab as delimiter
                # an examples is: 4	Miramar	B-LOC	-	stephen
                # tokens[0] = 4         : id
                # tokens[1] = Miramar   : token
                # tokens[2] = B-LOC     : ner tag
                # tokens[3] = -         : -
                # tokens[4] = stephen   : annotator
                splits = line.split("\t")
                tokens.append(splits[1])
                ner_tag = splits[2].rstrip()
                if ner_tag == "B-OTH" or ner_tag == "I-OTH":
                    ner_tag = "O"
                ner_tags.append(ner_tag)
        # last example        
        if tokens:
            dataset_words.append(tokens)
            dataset_labels.append(ner_tags)

    print(f"Read {len(dataset_words)} sentences from {filepath}")
    dataset_labels = [rewrite_labels(labels, encoding="iob2") for labels in dataset_labels]
    return dataset_words, dataset_labels



def load_uner_tsv(
    path: str,
    ENTITY_TO_CLASS_MAPPING: Dict[str, Type[Entity]],
) -> Tuple[List[List[str]], List[List[Entity]]]:
    """
    Load the uner dataset from a tsv file
    Args:
        path (str): The path to the tsv file
    Returns:
        (List[str],List[Union[Location,Organization,Person,Miscellaneous]]): The text and the entities
    """
    dataset_sentences: List[List[str]] = []
    dataset_entities: List[List[Entity]] = []

    dataset_words, dataset_labels = read_tsv(path)

    for words, labels in zip(dataset_words, dataset_labels):
        labels = rewrite_labels(labels=labels, encoding="iob2")
        # Get labeled word spans
        spans = []
        for i, label in enumerate(labels):
            if label == "O":
                continue
            elif label.startswith("B-"):
                spans.append([label[2:], i, i + 1])
            elif label.startswith("I-"):
                spans[-1][2] += 1
            else:
                raise ValueError(f"Found an unexpected label: {label}")

        # Get entities
        entities = []
        for label, start, end in spans:
            if label.lower() != "misc":
                entities.append(ENTITY_TO_CLASS_MAPPING[label](span=" ".join(words[start:end])))

        dataset_sentences.append(words)
        dataset_entities.append(entities)

    return dataset_sentences, dataset_entities


class UNERDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the UNER dataset.

    Args:
        path_or_split (`str`):
            The split to load. Can be one of `train`, `validation` or `test`. Or the path to a
            tsv file in conll format.
            Whether to include the MISC entity type. Defaults to `True`.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    ENTITY_TO_CLASS_MAPPING = None

    def __init__(self, path_or_split: str, **kwargs) -> None:
        self.ENTITY_TO_CLASS_MAPPING = {        
                "LOC": Location,
                "ORG": Organization,
                "PER": Person,
            }
    

        self.elements = {}

        dataset_words, dataset_entities = load_uner_tsv(
            path=path_or_split,
            ENTITY_TO_CLASS_MAPPING=self.ENTITY_TO_CLASS_MAPPING,
        )

        for id, (words, entities) in enumerate(zip(dataset_words, dataset_entities)):
            self.elements[id] = {
                "id": id,
                "doc_id": id,
                "text": " ".join(words),
                "entities": entities,
                "gold": entities,
            }

def load_translation(language):
    path = f"data_translatetest/uner/uner_{language}_eng_Latn.jsonl"
    with open(path, "r", encoding="utf-8") as f:
        data = [json.loads(l)["output_sentence"] for l in f]
    return data


class UNERTransFusionDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the UNER dataset.

    Args:
        path_or_split (`str`):
            The split to load. Can be one of `train`, `validation` or `test`. Or the path to a
            tsv file in conll format.
            Whether to include the MISC entity type. Defaults to `True`.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    ENTITY_TO_CLASS_MAPPING = None

    def __init__(self, path_or_split: str, **kwargs) -> None:
        self.ENTITY_TO_CLASS_MAPPING = {        
                "LOC": Location,
                "ORG": Organization,
                "PER": Person,
            }
    

        self.elements = {}

        dataset_words, dataset_entities = load_uner_tsv(
            path=path_or_split,
            ENTITY_TO_CLASS_MAPPING=self.ENTITY_TO_CLASS_MAPPING,
        )
        
        language= path_or_split.split("/")[-1].replace("-ud-test.iob2", "")
        translation = load_translation(language=language)
        
        for id, (words, entities, eng_text) in enumerate(zip(dataset_words, dataset_entities, translation)):
        
            self.elements[id] = {
                "id": id,
                "doc_id": id,
                "text": " ".join(words),
                "en_text": eng_text,
                "entities": entities,
                "en_entities": [],
                "gold": entities,
                "en_gold": [],
            }

class UNERSampler(Sampler):
    """
    A data `Sampler` for the UNER dataset.

    Args:
        dataset_loader (`UNERDatasetLoader`):
            The dataset loader that contains the data information.
        task (`str`, optional):
            The task to sample. It must be one of the following: NER, VER, RE, EE.
            Defaults to `None`.
        split (`str`, optional):
            The path_or_split to sample. It must be one of the following: "train", "dev" or
            "test". Depending on the path_or_split the sampling strategy differs. Defaults to
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
        dataset_loader: UNERDatasetLoader,
        task: str = None,
        split: str = "train",
        parallel_instances: Union[int, Tuple[int, int]] = 1,
        max_guidelines: int = -1,
        guideline_dropout: float = 0.0,
        seed: float = 0,
        prompt_template: str = "templates/prompt.txt",
        ensure_positives_on_train: bool = False,
        dataset_name: str = None,
        scorer: str = None,
        sample_only_gold_guidelines: bool = False,
        use_transfusion: bool = False,
        **kwargs,
    ) -> None:
        assert task in [
            "NER",
        ], f"UNER only supports NER task. {task} is not supported."

        task_definitions, task_target = ENTITY_DEFINITIONS_woMISC, "entities"

        super().__init__(
            dataset_loader=dataset_loader,
            task=task,
            split=split,
            parallel_instances=parallel_instances,
            max_guidelines=max_guidelines,
            guideline_dropout=guideline_dropout,
            seed=seed,
            prompt_template=prompt_template,
            ensure_positives_on_train=ensure_positives_on_train,
            sample_only_gold_guidelines=sample_only_gold_guidelines,
            dataset_name=dataset_name,
            scorer=scorer,
            task_definitions=task_definitions,
            task_target=task_target,
            definitions=GUIDELINES,
            examples=EXAMPLES,
            use_transfusion=use_transfusion,
            **kwargs,
        )
