import inspect
import json
from typing import Tuple, Union

from src.tasks.ace.guidelines import GUIDELINES
from src.tasks.ace.guidelines_gold import EXAMPLES
from src.tasks.ace.prompts import (
    COARSE_EVENT_DEFINITIONS,
    COARSE_RELATION_DEFINITIONS,
    COARSE_TO_FINE_EVENTS,
    COARSE_TO_FINE_RELATIONS,
    ENTITY_DEFINITIONS,
    EVENT_DEFINITIONS,
    FINE_TO_COARSE_EVENTS,
    FINE_TO_COARSE_RELATIONS,
    GPE,
    RELATION_DEFINITIONS,
    VALUE_DEFINITIONS,
    Acquit,
    AgentArtifactRelationRelation,
    Appeal,
    ArrestJail,
    Attack,
    BeBorn,
    Business,
    BusinessEvent,
    ChargeIndict,
    CitizenResidentReligionEthnicity,
    ConflictEvent,
    ContactEvent,
    ContactInfo,
    Convict,
    Crime,
    DeclareBankruptcy,
    Demonstrate,
    Die,
    Divorce,
    Elect,
    Employment,
    EndOrg,
    EndPosition,
    Execute,
    Extradite,
    Facility,
    Family,
    Fine,
    Founder,
    GenAffiliationRelation,
    Geographical,
    Injure,
    InvestorShareholder,
    JobTitle,
    JusticeEvent,
    LastingPersonal,
    LifeEvent,
    Located,
    Location,
    Marry,
    Meet,
    Membership,
    MergeOrg,
    MovementEvent,
    Near,
    Nominate,
    Numeric,
    Organization,
    OrganizationAffiliationRelation,
    OrgLocationOrigin,
    Ownership,
    Pardon,
    PartWholeRelation,
    Person,
    PersonalSocialRelation,
    PersonnelEvent,
    PhoneWrite,
    PhysicalRelation,
    ReleaseParole,
    Sentence,
    SentenceAct,
    SportsAffiliation,
    StartOrg,
    StartPosition,
    StudentAlum,
    Subsidiary,
    Sue,
    Time,
    TransactionEvent,
    TransferMoney,
    TransferOwnership,
    Transport,
    TrialHearing,
    UserOwnerInventorManufacturer,
    Vehicle,
    Weapon,
)

from ..utils_data import DatasetLoader, Sampler
from src.tasks.ace.easyproject_data import decode_data

ENTITY_TO_CLASS_MAPPING = {
        "FAC": Facility,
        "GPE": GPE,
        "LOC": Location,
        "ORG": Organization,
        "PER": Person,
        "VEH": Vehicle,
        "WEA": Weapon,
    }
VALUE_TO_CLASS_MAPPING = {
        "Contact-Info": ContactInfo,
        "Crime": Crime,
        "Job-Title": JobTitle,
        "Numeric": Numeric,
        "Sentence": Sentence,
        "TIME": Time,
    }
    # RELATION_TO_CLASS_MAPPING = {
    #     "ART:User-Owner-Inventor-Manufacturer": (AgentArtifactRelationRelation, UserOwnerInventorManufacturer),
    #     "GEN-AFF:Citizen-Resident-Religion-Ethnicity": (GenAffiliationRelation, CitizenResidentReligionEthnicity),
    #     "GEN-AFF:Org-Location": (GenAffiliationRelation, OrgLocationOrigin),
    #     "ORG-AFF:Employment": (OrganizationAffiliationRelation, Employment),
    #     "ORG-AFF:Founder": (OrganizationAffiliationRelation, Founder),
    #     "ORG-AFF:Investor-Shareholder": (OrganizationAffiliationRelation, InvestorShareholder),
    #     "ORG-AFF:Membership": (OrganizationAffiliationRelation, Membership),
    #     "ORG-AFF:Ownership": (OrganizationAffiliationRelation, Ownership),
    #     "ORG-AFF:Sports-Affiliation": (OrganizationAffiliationRelation, SportsAffiliation),
    #     "ORG-AFF:Student-Alum": (OrganizationAffiliationRelation, StudentAlum),
    #     "PART-WHOLE:Artifact": (
    #         PartWholeRelation,
    #         Geographical,
    #     ),  # There is no definition for Artifact relation on the guidelines
    #     "PART-WHOLE:Geographical": (PartWholeRelation, Geographical),
    #     "PART-WHOLE:Subsidiary": (PartWholeRelation, Subsidiary),
    #     "PER-SOC:Business": (PersonalSocialRelation, Business),
    #     "PER-SOC:Family": (PersonalSocialRelation, Family),
    #     "PER-SOC:Lasting-Personal": (PersonalSocialRelation, LastingPersonal),
    #     "PHYS:Located": (PhysicalRelation, Located),
    #     "PHYS:Near": (PhysicalRelation, Near),
    # }
RELATION_TO_CLASS_MAPPING = {
        "ART": AgentArtifactRelationRelation,
        "GEN-AFF": GenAffiliationRelation,
        "ORG-AFF": OrganizationAffiliationRelation,
        "PART-WHOLE": PartWholeRelation, # There is no definition for Artifact relation on the guidelines
        "PER-SOC": PersonalSocialRelation,
        "PHYS": PhysicalRelation,
        
    }
_EVENT_CONSTANTS_MAPPING = {
        "trigger": "mention",
        "Place": "place",
        "Time-After": "time",
        "Time-At-Begginning": "time",
        "Time-At-Beginning": "time",  # A bug on the data
        "Time-At-End": "time",
        "Time-Before": "time",
        "Time-Ending": "time",
        "Time-Holds": "time",
        "Time-Starting": "time",
        "Time-Within": "time",
    }
EVENT_TO_CLASS_MAPPING = {
        "Business:Declare-Bankruptcy": {
            "coarse": BusinessEvent,
            "class": DeclareBankruptcy,
            "Org": "org",
        },
        "Business:End-Org": {
            "coarse": BusinessEvent,
            "class": EndOrg,
            "Org": "org",
        },
        "Business:Merge-Org": {
            "coarse": BusinessEvent,
            "class": MergeOrg,
            "Org": "org",
        },
        "Business:Start-Org": {"coarse": BusinessEvent, "class": StartOrg, "Agent": "agent", "Org": "org"},
        "Conflict:Attack": {
            "coarse": ConflictEvent,
            "class": Attack,
            "Agent": "attacker",
            "Attacker": "attacker",
            "Instrument": "instrument",
            "Target": "target",
            "Victim": "target",
        },
        "Conflict:Demonstrate": {
            "coarse": ConflictEvent,
            "class": Demonstrate,
            "Entity": "entity",
        },
        "Contact:Meet": {
            "coarse": ContactEvent,
            "class": Meet,
            "Entity": "entity",
        },
        "Contact:Phone-Write": {
            "coarse": ContactEvent,
            "class": PhoneWrite,
            "Entity": "entity",
        },
        "Justice:Acquit": {
            "coarse": JusticeEvent,
            "class": Acquit,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Defendant": "defendant",
        },
        "Justice:Appeal": {
            "coarse": JusticeEvent,
            "class": Appeal,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Plaintiff": "prosecutor",
        },
        "Justice:Arrest-Jail": {
            "coarse": JusticeEvent,
            "class": ArrestJail,
            "Agent": "agent",
            "Crime": "crime",
            "Person": "person",
        },
        "Justice:Charge-Indict": {
            "coarse": JusticeEvent,
            "class": ChargeIndict,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Defendant": "defendant",
            "Prosecutor": "prosecutor",
        },
        "Justice:Convict": {
            "coarse": JusticeEvent,
            "class": Convict,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Defendant": "defendant",
        },
        "Justice:Execute": {
            "coarse": JusticeEvent,
            "class": Execute,
            "Agent": "agent",
            "Crime": "crime",
            "Person": "person",
        },
        "Justice:Extradite": {
            "coarse": JusticeEvent,
            "class": Extradite,
            "Agent": "agent",
            "Destination": "destination",
            "Origin": "origin",
            "Person": "person",
        },
        "Justice:Fine": {
            "coarse": JusticeEvent,
            "class": Fine,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Entity": "entity",
            "Money": "money",
        },
        "Justice:Pardon": {
            "coarse": JusticeEvent,
            "class": Pardon,
            "Adjudicator": "adjudicator",
            "Defendant": "defendant",
            "Crime": "crime",
        },
        "Justice:Release-Parole": {
            "coarse": JusticeEvent,
            "class": ReleaseParole,
            "Crime": "crime",
            "Entity": "entity",
            "Person": "person",
        },
        "Justice:Sentence": {
            "coarse": JusticeEvent,
            "class": SentenceAct,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Defendant": "defendant",
            "Sentence": "sentence",
        },
        "Justice:Sue": {
            "coarse": JusticeEvent,
            "class": Sue,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Defendant": "defendant",
            "Plaintiff": "plaintiff",
        },
        "Justice:Trial-Hearing": {
            "coarse": JusticeEvent,
            "class": TrialHearing,
            "Adjudicator": "adjudicator",
            "Crime": "crime",
            "Defendant": "defendant",
            "Prosecutor": "prosecutor",
        },
        "Life:Be-Born": {
            "coarse": LifeEvent,
            "class": BeBorn,
            "Person": "person",
        },
        "Life:Die": {
            "coarse": LifeEvent,
            "class": Die,
            "Agent": "agent",
            "Instrument": "instrument",
            "Person": "victim",
            "Victim": "victim",
        },
        "Life:Divorce": {
            "coarse": LifeEvent,
            "class": Divorce,
            "Person": "person",
        },
        "Life:Injure": {
            "coarse": LifeEvent,
            "class": Injure,
            "Agent": "agent",
            "Instrument": "instrument",
            "Victim": "victim",
        },
        "Life:Marry": {
            "coarse": LifeEvent,
            "class": Marry,
            "Person": "person",
        },
        "Movement:Transport": {
            "coarse": MovementEvent,
            "class": Transport,
            "Agent": "agent",
            "Artifact": "artifact",
            "Destination": "destination",
            "Origin": "origin",
            "Place": "destination",
            "Vehicle": "vehicle",
            "Victim": "artifact",  # MMMmmm WTF
            "Price": "price",
        },
        "Personnel:Elect": {
            "coarse": PersonnelEvent,
            "class": Elect,
            "Entity": "entity",
            "Person": "person",
            "Position": "position",
        },
        "Personnel:End-Position": {
            "coarse": PersonnelEvent,
            "class": EndPosition,
            "Entity": "entity",
            "Person": "person",
            "Position": "position",
        },
        "Personnel:Nominate": {
            "coarse": PersonnelEvent,
            "class": Nominate,
            "Agent": "agent",
            "Person": "person",
            "Position": "position",
        },
        "Personnel:Start-Position": {
            "coarse": PersonnelEvent,
            "class": StartPosition,
            "Entity": "entity",
            "Person": "person",
            "Position": "position",
        },
        "Transaction:Transfer-Money": {
            "coarse": TransactionEvent,
            "class": TransferMoney,
            "Beneficiary": "beneficiary",
            "Giver": "giver",
            "Money": "money",
            "Recipient": "recipient",
        },
        "Transaction:Transfer-Ownership": {
            "coarse": TransactionEvent,
            "class": TransferOwnership,
            "Artifact": "artifact",
            "Beneficiary": "beneficiary",
            "Buyer": "buyer",
            "Price": "price",
            "Seller": "seller",
        },
    }

class ACEDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the ACE05 dataset.

    Args:
        path (`str`):
            The location of the dataset directory.
        group_by (`str`, optional):
            Whether to group the texts by sentence or documents. Defaults to "sentence".

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    def __init__(self, path: str, group_by: str = "sentence", **kwargs) -> None:
        assert group_by in [
            "sentence",
            "document",
        ], "`group_by` must be either 'sentence' or 'document'."

        self.elements = {}

        with open(path, "rt") as in_f:
            for line in in_f:
                line = json.loads(line.strip())

                key = line["wnd_id"] if group_by == "sentence" else line["doc_id"]
                if key not in self.elements:
                    self.elements[key] = {
                        "id": key,
                        "doc_id": line["doc_id"],
                        "text": "",
                        "entities": [],
                        "values": [],
                        "coarse_relations": [],
                        "relations": [],
                        "events": [],
                        "arguments": [],
                        "gold": [],
                    }

                entities = [
                    ENTITY_TO_CLASS_MAPPING[entity["entity_type"]](span=entity["text"])
                    for entity in line["entity_mentions"]
                    if entity["entity_type"] in ENTITY_TO_CLASS_MAPPING
                ]
                values = [
                    VALUE_TO_CLASS_MAPPING[entity["entity_type"]](span=entity["text"])
                    for entity in line["entity_mentions"]
                    if entity["entity_type"] in VALUE_TO_CLASS_MAPPING
                ]
                coarse_relations, relations = [], []
                for rel in line["relation_mentions"]:
                    # if rel["relation_subtype"] not in self.RELATION_TO_CLASS_MAPPING:
                    #     continue
                    coarse_relations.append(
                        RELATION_TO_CLASS_MAPPING[rel["relation_type"]](
                            arg1=rel["arguments"][0]["text"],
                            arg2=rel["arguments"][1]["text"],
                        )
                    )
                    # relations.append(
                    #     self.RELATION_TO_CLASS_MAPPING[rel["relation_subtype"]][-1](
                    #         arg1=rel["arguments"][0]["text"],
                    #         arg2=rel["arguments"][1]["text"],
                    #     )
                    # )
                events, arguments = [], []
                for event in line["event_mentions"]:
                    if event["event_type"] not in EVENT_TO_CLASS_MAPPING:
                        continue
                    info = EVENT_TO_CLASS_MAPPING[event["event_type"]]
                    _inst = {param: [] for param in inspect.signature(info["class"]).parameters.keys()}
                    _inst["mention"] = event["trigger"]["text"]
                    for argument in event["arguments"]:
                        if argument["role"] in info:
                            name = info[argument["role"]]
                            _inst[name].append(argument["text"])
                        elif argument["role"] in _EVENT_CONSTANTS_MAPPING:
                            name = _EVENT_CONSTANTS_MAPPING[argument["role"]]
                            if name not in _inst:
                                continue
                            _inst[name].append(argument["text"])
                        else:
                            raise ValueError(f"Argument {event['event_type']}:{argument['role']} not found!")

                    events.append(info["coarse"](mention=_inst["mention"]))
                    arguments.append(info["class"](**_inst))

                
                self.elements[key]["text"] += " " + line["sentence"].strip()
                self.elements[key]["entities"] += entities
                self.elements[key]["values"] += values
                self.elements[key]["coarse_relations"] += coarse_relations
                self.elements[key]["relations"] += relations
                self.elements[key]["events"] += events
                self.elements[key]["arguments"] += arguments
                self.elements[key]["gold"] += entities  

def make_events(spans, marker2label, annotation, entity_info, trigger_info):
    entities = []
    coarse_relations = []
    values = []
    events = []
    arguments = []

    for mark_idx, span in spans:
        label_id = marker2label[mark_idx]
        if label_id in entity_info:
            entity_info[label_id]["span"] = span

        if label_id in trigger_info:
            trigger_info[label_id]["span"] = span
        
    
    entities = [
            ENTITY_TO_CLASS_MAPPING[entity["entity_type"]](span=entity["span"])
            for _id, entity in entity_info.items()
            if entity["entity_type"] in ENTITY_TO_CLASS_MAPPING
            ]

    values = [
    ]
    
    coarse_relations, relations = [], []
    for rel in annotation["relation_mentions"]:
        # if rel["relation_subtype"] not in self.RELATION_TO_CLASS_MAPPING:
        #     continue
        arg1_id = rel["arguments"][0]["entity_id"]
        arg2_id = rel["arguments"][1]["entity_id"]

        coarse_relations.append(
            RELATION_TO_CLASS_MAPPING[rel["relation_type"]](
                arg1=entity_info[arg1_id]["span"],
                arg2=entity_info[arg2_id]["span"],
            )
        )
        
    events, arguments = [], []
    for event in annotation["event_mentions"]:
        if event["event_type"] not in EVENT_TO_CLASS_MAPPING:
            continue
        info = EVENT_TO_CLASS_MAPPING[event["event_type"]]
        _inst = {param: [] for param in inspect.signature(info["class"]).parameters.keys()}
        event_id = event["id"]
        _inst["mention"] = trigger_info[event_id]["span"]
        for argument in event["arguments"]:
            if argument["role"] in info:
                name = info[argument["role"]]
                arg_id = argument["entity_id"]
                _inst[name].append(entity_info[arg_id]["span"])
            elif argument["role"] in _EVENT_CONSTANTS_MAPPING:
                name = _EVENT_CONSTANTS_MAPPING[argument["role"]]
                if name not in _inst:
                    continue
                arg_id = argument["entity_id"]
                _inst[name].append(entity_info[arg_id]["span"])
            else:
                raise ValueError(f"Argument {event['event_type']}:{argument['role']} not found!")

        events.append(info["coarse"](mention=_inst["mention"]))
        arguments.append(info["class"](**_inst))
    return entities, coarse_relations, values, events, arguments

class ACETranslationDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the ACE05 dataset.

    Args:
        path (`str`):
            The location of the dataset directory.
        group_by (`str`, optional):
            Whether to group the texts by sentence or documents. Defaults to "sentence".

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    def __init__(self, path: str, group_by: str = "sentence", **kwargs) -> None:
        assert group_by in [
            "sentence",
            "document",
        ], "`group_by` must be either 'sentence' or 'document'."

        self.elements = {}
        key = 0
        with open(path, "rt", encoding="utf-8") as in_f:
            for line in in_f:
                line = json.loads(line.strip())
                
                input_sentence = line["input_sentence"]
                output_sentence = line["output_sentence"]
                marker2label = line["marker2label"]
                annotation = marker2label["annotation"]
                entity_info = {}
                trigger_info = {}
                for entity in annotation["entity_mentions"]:
                    entity_info[entity["id"]] = entity
                for event in annotation["event_mentions"]:
                    trigger_info[event["id"]] = event
                clean_sentence, spans = decode_data(input_sentence, output_sentence, marker2label)
                if (clean_sentence and spans) or (clean_sentence and spans == []):
                    # decode label
                    entities, coarse_relations, values, events, arguments = make_events(spans, marker2label, annotation, 
                                                                                        entity_info, trigger_info)

                    self.elements[key] = {}
                    self.elements[key]["id"] = key
                    self.elements[key]["doc_id"] = key
                    self.elements[key]["text"] = clean_sentence
                    self.elements[key]["entities"] = entities
                    self.elements[key]["values"] = values
                    self.elements[key]["coarse_relations"] = coarse_relations
                    self.elements[key]["relations"] = []
                    self.elements[key]["events"] = events
                    self.elements[key]["arguments"] = arguments
                    self.elements[key]["gold"] = entities  
                    key += 1

class ACETransFusionDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the ACE05 dataset.

    Args:
        path (`str`):
            The location of the dataset directory.
        group_by (`str`, optional):
            Whether to group the texts by sentence or documents. Defaults to "sentence".

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """

    def __init__(self, path: str, group_by: str = "sentence", **kwargs) -> None:
        assert group_by in [
            "sentence",
            "document",
        ], "`group_by` must be either 'sentence' or 'document'."

        self.elements = {}
        key = 0
        with open(path, "rt", encoding="utf-8") as in_f:
            for line in in_f:
                line = json.loads(line.strip())
                
                input_sentence = line["input_sentence"]
                output_sentence = line["output_sentence"]
                marker2label = line["marker2label"]
                annotation = marker2label["annotation"]
                entity_info = {}
                trigger_info = {}
                for entity in annotation["entity_mentions"]:
                    entity_info[entity["id"]] = entity
                for event in annotation["event_mentions"]:
                    trigger_info[event["id"]] = event
                clean_sentence, spans = decode_data(input_sentence, output_sentence, marker2label)
                clean_en_sentence, en_spans = decode_data(input_sentence, input_sentence, marker2label)
                if (clean_sentence and spans and clean_en_sentence and en_spans) or (clean_sentence and spans == [] and clean_en_sentence and en_spans == []):
                    # decode label
                    entities, coarse_relations, values, events, arguments = make_events(spans, marker2label, annotation,
                                                                                            entity_info, trigger_info)
                    en_entities, en_coarse_relations, en_values, en_events, en_arguments = make_events(en_spans, marker2label, annotation,
                                                                                            entity_info, trigger_info)

                    self.elements[key] = {}
                    self.elements[key]["id"] = key
                    self.elements[key]["doc_id"] = key
                    self.elements[key]["text"] = clean_sentence
                    self.elements[key]["en_text"] = clean_en_sentence
                    self.elements[key]["entities"] = entities
                    self.elements[key]["values"] = values
                    self.elements[key]["coarse_relations"] = coarse_relations
                    self.elements[key]["relations"] = []
                    self.elements[key]["events"] = events
                    self.elements[key]["arguments"] = arguments
                    self.elements[key]["gold"] = entities  
                    self.elements[key]["en_entities"] = en_entities
                    self.elements[key]["en_values"] = values
                    self.elements[key]["en_coarse_relations"] = en_coarse_relations
                    self.elements[key]["en_relations"] = []
                    self.elements[key]["en_events"] = en_events
                    self.elements[key]["en_arguments"] = en_arguments
                    self.elements[key]["en_gold"] = en_entities  
                    key += 1

class ACESampler(Sampler):
    """
    A data `Sampler` for the ACE05 dataset.

    Args:
        dataset_loader (`ACEDatasetLoader`):
            The dataset loader that contains the data information.
        task (`str`, optional):
            The task to sample. It must be one of the following: NER, VER, RE, EE.
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
        dataset_loader: ACEDatasetLoader,
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
        use_transfusionv2: bool = False,
        **kwargs,
    ) -> None:
        assert task in [
            "NER",
            "VER",
            "RE",
            "RC",
            "EE",
            "EAE",
        ], f"{task} must be either 'NER', 'VER', 'RE', 'RC', 'EE', 'EAE'."

        if use_transfusion:
            if use_transfusionv2:
                task_definitions, task_target, task_template = {
                    "NER": (ENTITY_DEFINITIONS, "entities", "templates/prompt_tfv2.txt"),
                    "VER": (VALUE_DEFINITIONS, "values", "templates/prompt_tfv2.txt"),
                    "RE": (COARSE_RELATION_DEFINITIONS, "coarse_relations", "templates/prompt_ace_re_tfv2.txt"),
                    "RC": (RELATION_DEFINITIONS, "relations", "templates/prompt_ace_rc_tfv2.txt"),
                    "EE": (COARSE_EVENT_DEFINITIONS, "events", "templates/prompt_tfv2.txt"),
                    "EAE": (EVENT_DEFINITIONS, "arguments", "templates/prompt_ace_eae_tfv2.txt"),
                }[task]
            else:
                task_definitions, task_target, task_template = {
                    "NER": (ENTITY_DEFINITIONS, "entities", "templates/prompt_tf.txt"),
                    "VER": (VALUE_DEFINITIONS, "values", "templates/prompt_tf.txt"),
                    "RE": (COARSE_RELATION_DEFINITIONS, "coarse_relations", "templates/prompt_ace_re_tfv2.txt"),
                    "RC": (RELATION_DEFINITIONS, "relations", "templates/prompt_ace_rc_tfv2.txt"),
                    "EE": (COARSE_EVENT_DEFINITIONS, "events", "templates/prompt_tf.txt"),
                    "EAE": (EVENT_DEFINITIONS, "arguments", "templates/prompt_ace_eae_tfv2.txt"),
                }[task]
        else:
            task_definitions, task_target, task_template = {
                "NER": (ENTITY_DEFINITIONS, "entities", "templates/prompt.txt"),
                "VER": (VALUE_DEFINITIONS, "values", "templates/prompt.txt"),
                "RE": (COARSE_RELATION_DEFINITIONS, "coarse_relations", "templates/prompt_ace_re.txt"),
                "RC": (RELATION_DEFINITIONS, "relations", "templates/prompt_ace_rc.txt"),
                "EE": (COARSE_EVENT_DEFINITIONS, "events", "templates/prompt.txt"),
                "EAE": (EVENT_DEFINITIONS, "arguments", "templates/prompt_ace_eae.txt"),
            }[task]

        if task in ["RC", "EAE"]:
            is_coarse_to_fine: bool = True
            COARSE_TO_FINE = COARSE_TO_FINE_EVENTS if task == "EAE" else COARSE_TO_FINE_RELATIONS
            FINE_TO_COARSE = FINE_TO_COARSE_EVENTS if task == "EAE" else FINE_TO_COARSE_RELATIONS
        else:
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
