from typing import List

from ..utils_typing import Entity, dataclass


"""Entity definitions

MultiCoNER
"""


@dataclass
class Person(Entity):
    """{ner_person}"""

    span: str  # {ner_person_examples}


@dataclass
class Corporation(Entity):
    """{ner_corporation}"""

    span: str  # {ner_corporation_examples}


@dataclass
class Location(Entity):
    """{ner_location}"""

    span: str  # {ner_location_examples}

@dataclass
class Groups(Entity):
    """{ner_groups}"""

    span: str  # {ner_groups_examples}

@dataclass
class Product(Entity):
    """{ner_product}"""

    span: str  # {ner_product_examples}

@dataclass
class CreativeWork(Entity):
    """{ner_creative_work}"""

    span: str  # {ner_creative_work_examples}


ENTITY_DEFINITIONS: List[Entity] = [
    Person,
    Corporation,
    Location,
    Groups,
    Product,
    CreativeWork,
    
]


# __all__ = list(map(str, [*ENTITY_DEFINITIONS]))
