import inspect
import json
from typing import Tuple, Union

from src.tasks.redfm.guidelines import GUIDELINES
from src.tasks.redfm.guidelines_gold import EXAMPLES
from src.tasks.redfm.prompts import (
    Celestial,
    Concept,
    Date,
    Distinct,
    Event,
    Location,
    Media,
    MISC,
    Organization,
    Person,
    Time,
    CountryRelation,
    PlaceOfBirthRelation,
    SpouseRelation,
    CountryOfCitizenshipRelation,
    CapitalRelation,
    InstanceOfRelation,
    ChildRelation,
    ShareBorderWithRelation,
    AuthorRelation,
    DirectorRelation,
    OccupationRelation,
    FoundedByRelation,
    LeagueRelation,
    OwnedByelation,
    GenreRelation,
    NamedAfterRelation,
    FollowsRelation,
    HeadquartersLocationRelation,
    CastMemberRelation,
    ManufacturerRelation,
    LocatedInOrNextToBodyOfWaterRelation,
    LocationRelation,
    PartOfRelation,
    MouthOfTheWatercourseRelation,
    MemberOfRelation,
    SportRelation,
    CharactersRelation,
    ParticipantRelation,
    NotableWorkRelation,
    ReplacesRelation,
    SiblingRelation,
    InceptionRelation,
    RELATION_DEFINITIONS,
)

from ..utils_data import DatasetLoader, Sampler


class REDFMDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the REDFM dataset.

    Args:
        path (`str`):
            The location of the dataset directory.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    relation_list = ['country', 'place of birth', 'spouse', 'country of citizenship', 'instance of', 
                    'capital', 'child', 'shares border with', 'author', 'director', 'occupation', 
                    'founded by', 'league', 'owned by', 'genre', 'named after', 'follows', 'headquarters location',
                    'cast member', 'manufacturer', 'located in or next to body of water', 'location', 'part of', 
                    'mouth of the watercourse', 'member of', 'sport', 'characters', 'participant', 'notable work', 
                    'replaces', 'sibling', 'inception']
    
    relid2relation = {idx: rel for idx, rel in enumerate(relation_list)}

    RELATION_TO_CLASS_MAPPING = {
            "country": CountryRelation,
            "place of birth": PlaceOfBirthRelation,
            "spouse": SpouseRelation,
            "country of citizenship": CountryOfCitizenshipRelation,
            "capital": CapitalRelation,
            "instance of": InstanceOfRelation,
            "child": ChildRelation,
            "shares border with": ShareBorderWithRelation,
            "author": AuthorRelation,
            "director": DirectorRelation,
            "occupation": OccupationRelation,
            "founded by": FoundedByRelation,
            "league": LeagueRelation,
            "owned by": OwnedByelation,
            "genre": GenreRelation,
            "named after": NamedAfterRelation,
            "follows": FollowsRelation,
            "headquarters location": HeadquartersLocationRelation,
            "cast member": CastMemberRelation,
            "manufacturer": ManufacturerRelation,
            "located in or next to body of water": LocatedInOrNextToBodyOfWaterRelation,
            "location": LocationRelation,
            "part of": PartOfRelation,
            "mouth of the watercourse": MouthOfTheWatercourseRelation,
            "member of": MemberOfRelation,
            "sport": SportRelation,
            "characters": CharactersRelation,
            "participant": ParticipantRelation,
            "notable work": NotableWorkRelation,
            "replaces": ReplacesRelation,
            "sibling": SiblingRelation,
            "inception": InceptionRelation
    }
    
    ENTITY_TO_CLASS_MAPPING = {
            "CEL": Celestial,
            "Concept": Concept,
            "DATE": Date,
            "DIS": Distinct,
            "EVE": Event,
            "LOC": Location,
            "MEDIA": Media,
            "MISC": MISC,
            "ORG": Organization,
            "PER": Person,
            "TIME": Time,
    }

    ENT_LIST = set(ENTITY_TO_CLASS_MAPPING.keys())

    def __init__(self, split: str, **kwargs) -> None:
        self.elements = {}

        from datasets import load_dataset

        dataset = load_dataset("Babelscape/REDFM", 
                kwargs["language"])
        
        for key, instance in enumerate(dataset[split]):
            self.elements[key] = {}
            text = instance["text"]

            entities = []
            for ent in instance["entities"]:
                ent_type = ent["type"]
                span = ent["surfaceform"]
                if ent_type in self.ENT_LIST:
                    entities.append(
                        self.ENTITY_TO_CLASS_MAPPING[ent_type](
                            span=span,
                        )
                    )
            relations = []
            for rel in instance["relations"]:
                rel_type = self.relid2relation[rel["predicate"]]
                subject_n = rel["subject"]["surfaceform"]
                object_n = rel["object"]["surfaceform"]
                relations.append(
                    self.RELATION_TO_CLASS_MAPPING[rel_type](
                        arg1=subject_n,
                        arg2=object_n,
                    )
                )
            self.elements[key]["id"] = key
            self.elements[key]["doc_id"] = key
            self.elements[key]["text"] = text
            self.elements[key]["entities"] = entities
            self.elements[key]["relations"] = relations
            self.elements[key]["gold"] = entities

def load_translation(language):
    path = f"data_translatetest/redfm/redfm_{language}_eng_Latn.jsonl"
    with open(path.format(language), "r", encoding="utf-8") as f:
        data = [json.loads(l)["output_sentence"] for l in f]
    return data

class REDFMTransFusionDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the REDFM dataset.

    Args:
        path (`str`):
            The location of the dataset directory.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    relation_list = ['country', 'place of birth', 'spouse', 'country of citizenship', 'instance of', 
                    'capital', 'child', 'shares border with', 'author', 'director', 'occupation', 
                    'founded by', 'league', 'owned by', 'genre', 'named after', 'follows', 'headquarters location',
                    'cast member', 'manufacturer', 'located in or next to body of water', 'location', 'part of', 
                    'mouth of the watercourse', 'member of', 'sport', 'characters', 'participant', 'notable work', 
                    'replaces', 'sibling', 'inception']
    
    relid2relation = {idx: rel for idx, rel in enumerate(relation_list)}

    RELATION_TO_CLASS_MAPPING = {
            "country": CountryRelation,
            "place of birth": PlaceOfBirthRelation,
            "spouse": SpouseRelation,
            "country of citizenship": CountryOfCitizenshipRelation,
            "capital": CapitalRelation,
            "instance of": InstanceOfRelation,
            "child": ChildRelation,
            "shares border with": ShareBorderWithRelation,
            "author": AuthorRelation,
            "director": DirectorRelation,
            "occupation": OccupationRelation,
            "founded by": FoundedByRelation,
            "league": LeagueRelation,
            "owned by": OwnedByelation,
            "genre": GenreRelation,
            "named after": NamedAfterRelation,
            "follows": FollowsRelation,
            "headquarters location": HeadquartersLocationRelation,
            "cast member": CastMemberRelation,
            "manufacturer": ManufacturerRelation,
            "located in or next to body of water": LocatedInOrNextToBodyOfWaterRelation,
            "location": LocationRelation,
            "part of": PartOfRelation,
            "mouth of the watercourse": MouthOfTheWatercourseRelation,
            "member of": MemberOfRelation,
            "sport": SportRelation,
            "characters": CharactersRelation,
            "participant": ParticipantRelation,
            "notable work": NotableWorkRelation,
            "replaces": ReplacesRelation,
            "sibling": SiblingRelation,
            "inception": InceptionRelation
    }
    
    ENTITY_TO_CLASS_MAPPING = {
            "CEL": Celestial,
            "Concept": Concept,
            "DATE": Date,
            "DIS": Distinct,
            "EVE": Event,
            "LOC": Location,
            "MEDIA": Media,
            "MISC": MISC,
            "ORG": Organization,
            "PER": Person,
            "TIME": Time,
    }

    ENT_LIST = set(ENTITY_TO_CLASS_MAPPING.keys())

    def __init__(self, split: str, **kwargs) -> None:
        self.elements = {}

        from datasets import load_dataset

        dataset = load_dataset("Babelscape/REDFM", 
                kwargs["language"])
        
        # load translation
        translation = load_translation(language=kwargs["language"])

        for key, (instance, en_text) in enumerate(zip(dataset[split], translation)):
            self.elements[key] = {}
            text = instance["text"]

            entities = []
            for ent in instance["entities"]:
                ent_type = ent["type"]
                span = ent["surfaceform"]
                if ent_type in self.ENT_LIST:
                    entities.append(
                        self.ENTITY_TO_CLASS_MAPPING[ent_type](
                            span=span,
                        )
                    )
            relations = []
            for rel in instance["relations"]:
                rel_type = self.relid2relation[rel["predicate"]]
                subject_n = rel["subject"]["surfaceform"]
                object_n = rel["object"]["surfaceform"]
                relations.append(
                    self.RELATION_TO_CLASS_MAPPING[rel_type](
                        arg1=subject_n,
                        arg2=object_n,
                    )
                )
            self.elements[key]["id"] = key
            self.elements[key]["doc_id"] = key
            self.elements[key]["text"] = text
            self.elements[key]["en_text"] = en_text
            self.elements[key]["entities"] = entities
            self.elements[key]["relations"] = relations
            self.elements[key]["en_relations"] = []
            self.elements[key]["gold"] = entities
            self.elements[key]["en_gold"] = []

class REDFMSampler(Sampler):
    """
    A data `Sampler` for the REDFM dataset.

    Args:
        dataset_loader (`REDFMDatasetLoader`):
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
        dataset_loader: REDFMDatasetLoader,
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
            "RE",
        ], f"{task} must be either 'NER', 'RE'."

        if use_transfusion:
            task_definitions, task_target, task_template = {
                "RE": (RELATION_DEFINITIONS, "relations", "templates/prompt_re_tfv2.txt"),
            }[task]
        else:
            task_definitions, task_target, task_template = {
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
