from typing import Dict, List, Type

from ..utils_typing import Entity, Relation, dataclass

"""Entity definitions

The entity definitions are derived from the official CoNLL04 guidelines:
https://aclanthology.org/W04-2401/
https://aclanthology.org/C02-1151.pdf
"""


@dataclass
class Person(Entity):
    """{conll04_person}"""

    span: str  # {conll04_person_examples}


@dataclass
class Location(Entity):
    """{conll04_location}"""

    span: str  # {conll04_location_examples}

@dataclass
class Organization(Entity):
    """{conll04_organization}"""

    span: str  # {conll04_organization_examples}

@dataclass
class Other(Entity):
    """{conll04_other}"""

    span: str  # {conll04_other_examples}


ENTITY_DEFINITIONS: List[Type] = [
    Person,
    Location,
    Organization,
    Other,
]

"""Relation definitions

The relations definitions are derived from the oficial CoNLL04 guidelines:
https://aclanthology.org/W04-2401/
https://lavis.cs.hs-rm.de/storage/spert/public/datasets/conll04/
"""


@dataclass
class OrgBasedInRelation(Relation):
    """{conll04_orgbasedin}"""

    arg1: str
    arg2: str

@dataclass
class LocatedInRelation(Relation):
    """{conll04_locatedin}"""

    arg1: str
    arg2: str

@dataclass
class KillRelation(Relation):
    """{conll04_kill}"""

    arg1: str
    arg2: str

@dataclass
class LiveInRelation(Relation):
    """{conll04_livein}"""

    arg1: str
    arg2: str

@dataclass
class WorkForRelation(Relation):
    """{conll04_workfor}"""

    arg1: str
    arg2: str

RELATION_DEFINITIONS: List[Type] = [
    OrgBasedInRelation,
    LocatedInRelation,
    KillRelation,
    LiveInRelation,
    WorkForRelation,
]

# __all__ = list(map(str, [*ENTITY_DEFINITIONS, *RELATION_DEFINITIONS]))
