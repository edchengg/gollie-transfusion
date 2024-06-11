from typing import Dict, List, Tuple, Type, Union
import json
import re
from src.tasks.massive.guidelines import GUIDELINES
from src.tasks.massive.guidelines_gold import EXAMPLES
from src.tasks.massive.prompts import (
    ENTITY_DEFINITIONS,
    Time,
    Date,
    ColorType,
    HousePlace,
    ChangeAmount,
    ArtistName,
    MediaType,
    PlaceName,
    TimeZone,
    OrderType,
    FoodType,
    NewsTopic,
    SongName,
    MusicGenre,
    DeviceType,
    MealType,
    BusinessName,
    GeneralFrequency,
    WeatherDescriptor,
    PlayerSetting,
    JokeType,
    TimeOfDay,
    EventName,
    BusinessType,
    PlaylistName,
    MusicDescriptor,
    Person,
    AlarmType,
    AppName,
    CoffeeType,
    Relation,
    MovieName,
    DrinkType,
    TransportType,
    MusicAlbum,
    PersonalInfo,
    ListName,
    SportType,
    RadioName,
    PodcastName,
    AudiobookName,
    AudiobookAuthor,
    CookingType,
    Ingredient,
    GameName,
    PodcastDescriptor,
    MovieType,
    TransportAgency,
    TransportDescriptor,
    TransportName,
    CurrencyName,
    DefinitionWord,
    EmailFolder,
    GameType,
    EmailAddress
)
from src.tasks.label_encoding import rewrite_labels

from ..utils_data import DatasetLoader, Sampler
from ..utils_typing import Entity


ENTITY_TO_CLASS_MAPPING = ENTITY_CLASS_MAP = {
    "time": Time,
    "date": Date,
    "color_type": ColorType,
    "house_place": HousePlace,
    "change_amount": ChangeAmount,
    "artist_name": ArtistName,
    "media_type": MediaType,
    "place_name": PlaceName,
    "time_zone": TimeZone,
    "order_type": OrderType,
    "food_type": FoodType,
    "news_topic": NewsTopic,
    "song_name": SongName,
    "music_genre": MusicGenre,
    "device_type": DeviceType,
    "meal_type": MealType,
    "business_name": BusinessName,
    "general_frequency": GeneralFrequency,
    "weather_descriptor": WeatherDescriptor,
    "player_setting": PlayerSetting,
    "joke_type": JokeType,
    "timeofday": TimeOfDay,
    "event_name": EventName,
    "business_type": BusinessType,
    "playlist_name": PlaylistName,
    "music_descriptor": MusicDescriptor,
    "person": Person,
    "alarm_type": AlarmType,
    "app_name": AppName,
    "coffee_type": CoffeeType,
    "relation": Relation,
    "movie_name": MovieName,
    "drink_type": DrinkType,
    "transport_type": TransportType,
    "music_album": MusicAlbum,
    "personal_info": PersonalInfo,
    "list_name": ListName,
    "sport_type": SportType,
    "radio_name": RadioName,
    "podcast_name": PodcastName,
    "audiobook_name": AudiobookName,
    "audiobook_author": AudiobookAuthor,
    "cooking_type": CookingType,
    "ingredient": Ingredient,
    "game_name": GameName,
    "podcast_descriptor": PodcastDescriptor,
    "movie_type": MovieType,
    "transport_agency": TransportAgency,
    "transport_descriptor": TransportDescriptor,
    "transport_name": TransportName,
    "currency_name": CurrencyName,
    "definition_word": DefinitionWord,
    "email_folder": EmailFolder,
    "game_type": GameType,
    "email_address": EmailAddress
}

label_list = ['date', 'place_name', 'event_name', 'person', 'time', 'media_type', 'business_name', 'weather_descriptor', 'food_type', 'transport_type', 'artist_name', 'timeofday', 'list_name', 'relation', 'house_place', 'device_type', 'definition_word', 'music_genre', 'currency_name', 'news_topic', 'player_setting', 'song_name', 'radio_name', 'business_type', 'color_type', 'game_name', 'podcast_descriptor', 'audiobook_name', 'general_frequency', 'order_type', 'meal_type', 'podcast_name', 'playlist_name', 'personal_info', 'time_zone', 'joke_type', 'transport_agency', 'email_address', 'change_amount', 'cooking_type', 'music_descriptor', 'ingredient', 'app_name', 'audiobook_author', 'email_folder', 'coffee_type', 'transport_name', 'alarm_type', 'movie_type', 'movie_name', 'transport_descriptor', 'drink_type', 'music_album']
FILTER_LABEL_LIST = set(label_list[:])

def extract_span_and_label(sentence):
    # Regular expression pattern to match the label and content
    pattern = r'\[(.*?)\s*:\s*(.*?)\]'
    
    # Find all matches in the sentence
    matches = re.findall(pattern, sentence)
    
    # Create a list of dictionaries to store label and content pairs
    extracted_info = []
    
    for match in matches:
        label, content = match
        extracted_info.append({
            'label': label.strip(),
            'content': content.strip()
        })
    
    return extracted_info

def load_massive_hf(
    language: str,
    split: str,
    max_sentence: int,
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
    from datasets import load_dataset

    dataset_sentences: List[List[str]] = []
    dataset_entities: List[List[Entity]] = []

    dataset = load_dataset("AmazonScience/massive", language, split=split)

    for i in range(min(max_sentence, len(dataset))):
        sentence = dataset[i]["utt"]
        ann_sent = dataset[i]["annot_utt"]
        annotations = extract_span_and_label(ann_sent)
        entities = []

        for span in annotations:
            label = span["label"]
            content = span["content"]

            if label in FILTER_LABEL_LIST:
                entities.append(ENTITY_TO_CLASS_MAPPING[label](span=content))

        dataset_sentences.append(sentence)
        dataset_entities.append(entities)

    return dataset_sentences, dataset_entities


class MassiveDatasetLoader(DatasetLoader):
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

        dataset_words, dataset_entities = load_massive_hf(
                language=kwargs["language"],
                split="test",
                max_sentence=500,
                ENTITY_TO_CLASS_MAPPING=ENTITY_TO_CLASS_MAPPING,
            )

        for id, (words, entities) in enumerate(zip(dataset_words, dataset_entities)):
            self.elements[id] = {
                "id": id,
                "doc_id": id,
                "text": words,
                "entities": entities,
                "gold": entities,
            }

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        output = [json.loads(l)["output_sentence"] for l in f]
    return output


class MassiveTransFusionDatasetLoader(DatasetLoader):
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

        dataset_words, dataset_entities = load_massive_hf(
                language=kwargs["language"],
                split="test",
                max_sentence=500,
                ENTITY_TO_CLASS_MAPPING=ENTITY_TO_CLASS_MAPPING,
            )

        lang = kwargs["language"]
        translation = load_jsonl(f"data_translatetest/massive/{lang}.eng_Latn.jsonl")
        for id, (words, entities, en_trans) in enumerate(zip(dataset_words, dataset_entities, translation)):
            
            self.elements[id] = {
                "id": id,
                "doc_id": id,
                "text": words,
                "en_text": en_trans,
                "entities": entities,
                "en_entities": [],
                "gold": entities,
                "en_gold": [],
            }

class MassiveSampler(Sampler):
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
        dataset_loader: MassiveDatasetLoader,
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
