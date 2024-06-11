from typing import Dict, List, Tuple, Type, Union
import json
from src.tasks.xsid.guidelines import GUIDELINES
from src.tasks.xsid.guidelines_gold import EXAMPLES
from src.tasks.xsid.prompts import (
    ENTITY_DEFINITIONS,
    Location, 
    Datetime, 
    WeatherAttribute, 
    Reference, 
    ReminderTodo, 
    AlarmModifier, 
    RecurringDatetime,
    ReminderModifier, 
    Negation, 
    TimerAttributes,
    NewsType, 
    WeatherTemperatureUnit, 
    EntityName, 
    Playlist, 
    MusicItem, 
    Artist, 
    PartySizeNumber, 
    Sort, 
    RestaurantType, 
    RestaurantName, 
    ServedDish, 
    Facility, 
    PartySizeDescription, 
    Cuisine, 
    ConditionTemperature, 
    ConditionDescription, 
    Service, 
    Album, 
    Genre, 
    Track, 
    RatingValue, 
    BestRating, 
    RatingUnit, 
    ObjectName, 
    ObjectPartOfSeriesType, 
    ObjectSelect,
    ObjectType, 
    MovieName, 
    ObjectLocationType, 
    MovieType
)
from src.tasks.label_encoding import rewrite_labels

from ..utils_data import DatasetLoader, Sampler
from ..utils_typing import Entity


ENTITY_TO_CLASS_MAPPING = {
"location": Location,
"datetime": Datetime,
"weather/attribute": WeatherAttribute,
"reference": Reference,
"reminder/todo": ReminderTodo,
"alarm/alarm_modifier": AlarmModifier,
"recurring_datetime": RecurringDatetime,
"reminder/reminder_modifier": ReminderModifier,
"negation": Negation,
"timer/attributes": TimerAttributes,
"news/type": NewsType,
"weather/temperatureUnit": WeatherTemperatureUnit,
"entity_name": EntityName,
"playlist": Playlist,
"music_item": MusicItem,
"artist": Artist,
"party_size_number": PartySizeNumber,
"sort": Sort,
"restaurant_type": RestaurantType,
"restaurant_name": RestaurantName,
"served_dish": ServedDish,
"facility": Facility,
"party_size_description": PartySizeDescription,
"cuisine": Cuisine,
"condition_temperature": ConditionTemperature,
"condition_description": ConditionDescription,
"service": Service,
"album": Album,
"genre": Genre,
"track": Track,
"rating_value": RatingValue,
"best_rating": BestRating,
"rating_unit": RatingUnit,
"object_name": ObjectName,
"object_part_of_series_type": ObjectPartOfSeriesType,
"object_select": ObjectSelect,
"object_type": ObjectType,
"movie_name": MovieName,
"object_location_type": ObjectLocationType,
"movie_type": MovieType,
}

label_set = set() 
for i in list(ENTITY_TO_CLASS_MAPPING.keys()):
    label_set.add("B-{}".format(i))
    label_set.add("I-{}".format(i))
label_set.add("O")

def get_conll_hf(
    split: str,
    include_misc: bool,
    ENTITY_TO_CLASS_MAPPING: Dict[str, Type[Entity]],
) -> Tuple[List[List[str]], List[List[Entity]]]:
    """
    Get the conll dataset from the huggingface datasets library
    Args:
        split (str): The path_or_split to load. Can be one of `train`, `validation` or `test`.
        include_misc (bool): Whether to include the MISC entity type. Defaults to `True`.
    Returns:
        (List[str],List[Union[Location,Organization,Person,Miscellaneous]]): The text and the entities
    """
    from datasets import load_dataset

    dataset = load_dataset("conll2003")
    id2label = dict(enumerate(dataset["train"].features["ner_tags"].feature.names))
    dataset_sentences: List[List[str]] = []
    dataset_entities: List[List[Entity]] = []

    for example in dataset[split]:
        words = example["tokens"]
        # Some of the CoNLL02-03 datasets are in IOB1 format instead of IOB2,
        # we convert them to IOB2, so we don't have to deal with this later.
        labels = rewrite_labels(labels=[id2label[label] for label in example["ner_tags"]], encoding="iob2")

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
            if include_misc or label != "MISC":
                entities.append(ENTITY_TO_CLASS_MAPPING[label](span=" ".join(words[start:end])))

        dataset_sentences.append(words)
        dataset_entities.append(entities)

    return dataset_sentences, dataset_entities


def read_tsv(filepath):
    """
    READ tsv file in conll format
    Args:
        filepath: Path to the file
    Returns: List of words, List of labels
    """

    dataset_words = []
    dataset_labels = []
    with open(filepath, "r", encoding="utf-8") as f:
        words = []
        labels = []
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "" or line == "\n":
                if words:
                    dataset_words.append(words)
                    dataset_labels.append(labels)
                    words = []
                    labels = []
            else:
                try:
                    _, word, _, label = line.split()
                    
                except ValueError:
                    try:
                        word, label, _ = line.split()
                    except ValueError:
                        raise ValueError(f"Cannot path_or_split line: {line}")
                if word:
                    if label not in label_set:
                        label = "O"
                    words.append(word)
                    labels.append(label)
        if words:
            dataset_words.append(words)
            dataset_labels.append(labels)

    print(f"Read {len(dataset_words)} sentences from {filepath}")
    return dataset_words, dataset_labels


def load_conll_tsv(
    path: str,
    ENTITY_TO_CLASS_MAPPING: Dict[str, Type[Entity]],
) -> Tuple[List[List[str]], List[List[Entity]]]:
    """
    Load the conll dataset from a tsv file
    Args:
        path (str): The path to the tsv file
        include_misc (bool): Whether to include the MISC entity type. Defaults to `True`.
    Returns:
        (List[str],List[Union[Location,Organization,Person,Miscellaneous]]): The text and the entities
    """
    dataset_sentences: List[List[str]] = []
    dataset_entities: List[List[Entity]] = []

    dataset_words, dataset_labels = read_tsv(path)

    for words, labels in zip(dataset_words, dataset_labels):
        # Some of the CoNLL02-03 datasets are in IOB1 format instead of IOB2,
        # we convert them to IOB2, so we don't have to deal with this later.
        print(labels)
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
            
            entities.append(ENTITY_TO_CLASS_MAPPING[label](span=" ".join(words[start:end])))

        dataset_sentences.append(words)
        dataset_entities.append(entities)

    return dataset_sentences, dataset_entities


class XSIDDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the ConLL03 dataset.

    Args:
        path_or_split (`str`):
            The split to load. Can be one of `train`, `validation` or `test`. Or the path to a
            tsv file in conll format.
        include_misc (`str`, optional):
            Whether to include the MISC entity type. Defaults to `True`.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """


    def __init__(self, path_or_split: str, include_misc: bool = True, **kwargs) -> None:

        self.elements = {}

        dataset_words, dataset_entities = load_conll_tsv(
                path=path_or_split,
                ENTITY_TO_CLASS_MAPPING=ENTITY_TO_CLASS_MAPPING,
            )

        for id, (words, entities) in enumerate(zip(dataset_words, dataset_entities)):
            self.elements[id] = {
                "id": id,
                "doc_id": id,
                "text": " ".join(words),
                "entities": entities,
                "gold": entities,
            }

def get_entities(labels, words, ENTITY_TO_CLASS_MAPPING, include_misc=False):
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
        if include_misc or label.lower() != "misc":
            entities.append(ENTITY_TO_CLASS_MAPPING[label](span=" ".join(words[start:end])))
    return entities

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        output = [json.loads(l)["output_sentence"] for l in f]
    return output


class XSIDTransFusionDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the ConLL03 dataset.

    Args:
        path_or_split (`str`):
            The split to load. Can be one of `train`, `validation` or `test`. Or the path to a
            tsv file in conll format.
        include_misc (`str`, optional):
            Whether to include the MISC entity type. Defaults to `True`.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    def __init__(self, path_or_split: str, include_misc: bool = True, **kwargs) -> None:

        self.elements = {}

        dataset_words, dataset_entities = load_conll_tsv(
                path=path_or_split,
                ENTITY_TO_CLASS_MAPPING=ENTITY_TO_CLASS_MAPPING,
            )

        lang = path_or_split.split("/")[-1].split(".")[0]
        translation = load_jsonl(f"data_translatetest/xsid/{lang}.eng_Latn.jsonl")
        for id, (words, entities, en_trans) in enumerate(zip(dataset_words, dataset_entities, translation)):
            
            self.elements[id] = {
                "id": id,
                "doc_id": id,
                "text": " ".join(words),
                "en_text": en_trans,
                "entities": entities,
                "en_entities": [],
                "gold": entities,
                "en_gold": [],
            }

class XSIDSampler(Sampler):
    """
    A data `Sampler` for the CONLL03 dataset.

    Args:
        dataset_loader (`CoNLLDatasetLoader`):
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
        dataset_loader: XSIDDatasetLoader,
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
        ], f"CoNLL03 only supports NER task. {task} is not supported."

        task_definitions, task_target = {
            "NER": (ENTITY_DEFINITIONS, "entities"),
        }[task]

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
