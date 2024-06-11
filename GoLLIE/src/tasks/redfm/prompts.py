from typing import Dict, List, Type

from ..utils_typing import Entity, Relation, dataclass

"""Entity definitions

{'CEL',
 'Concept',
 'DATE',
 'DIS',
 'EVE',
 'LOC',
 'MEDIA',
 'MISC',
 'ORG',
 'PER',
 'TIME'}
"""

@dataclass
class Celestial(Entity):
    """{redfm_cel}"""
    span: str # {redfm_cel_examples}

@dataclass
class Concept(Entity):
    """{redfm_concept}"""
    span: str # {redfm_concept_examples}

@dataclass
class Date(Entity):
    """{redfm_date}"""
    span: str # {redfm_date_examples}

@dataclass
class Distinct(Entity):
    """{redfm_dis}"""
    span: str # {redfm_dis_examples}

@dataclass
class Event(Entity):
    """{redfm_eve}"""
    span: str # {redfm_eve_examples}

@dataclass
class Location(Entity):
    """{redfm_loc}"""
    span: str # {redfm_loc_examples}

@dataclass
class Media(Entity):
    """{redfm_media}"""
    span: str # {redfm_media_examples}

@dataclass
class MISC(Entity):
    """{redfm_misc}"""
    span: str # {redfm_misc_examples}

@dataclass
class Organization(Entity):
    """{redfm_org}"""
    span: str # {redfm_org_examples}

@dataclass
class Person(Entity):
    """{redfm_per}"""
    span: str # {redfm_per_examples}

@dataclass
class Time(Entity):
    """{redfm_time}"""
    span: str # {redfm_time_examples}


"""Relation definitions

The relations definitions are derived from the REDFM guidelines:
['country', 'place of birth', 'spouse', 'country of citizenship', 'instance of', 
'capital', 'child', 'shares border with', 'author', 'director', 'occupation', 
'founded by', 'league', 'owned by', 'genre', 'named after', 'follows', 'headquarters location',
 'cast member', 'manufacturer', 'located in or next to body of water', 'location', 'part of', 
 'mouth of the watercourse', 'member of', 'sport', 'characters', 'participant', 'notable work', 
 'replaces', 'sibling', 'inception']
"""


@dataclass
class CountryRelation(Relation):
    """{redfm_country}"""

    arg1: str
    arg2: str

@dataclass
class PlaceOfBirthRelation(Relation):
    """{redfm_placeofbirth}"""

    arg1: str
    arg2: str

@dataclass
class SpouseRelation(Relation):
    """{redfm_spouse}"""

    arg1: str
    arg2: str

@dataclass
class CountryOfCitizenshipRelation(Relation):
    """{redfm_citizenship}"""

    arg1: str
    arg2: str

@dataclass
class CapitalRelation(Relation):
    """{redfm_capital}"""

    arg1: str
    arg2: str

@dataclass
class InstanceOfRelation(Relation):
    """{redfm_instanceof}"""

    arg1: str
    arg2: str

@dataclass
class ChildRelation(Relation):
    """{redfm_child}"""

    arg1: str
    arg2: str

@dataclass
class ShareBorderWithRelation(Relation):
    """{redfm_shareborderwith}"""

    arg1: str
    arg2: str

@dataclass
class AuthorRelation(Relation):
    """{redfm_author}"""

    arg1: str
    arg2: str

@dataclass
class DirectorRelation(Relation):
    """{redfm_director}"""

    arg1: str
    arg2: str

@dataclass
class OccupationRelation(Relation):
    """{redfm_occupation}"""

    arg1: str
    arg2: str

@dataclass
class FoundedByRelation(Relation):
    """{redfm_foundedby}"""

    arg1: str
    arg2: str

@dataclass
class LeagueRelation(Relation):
    """{redfm_league}"""

    arg1: str
    arg2: str

@dataclass
class OwnedByelation(Relation):
    """{redfm_ownedby}"""

    arg1: str
    arg2: str

@dataclass
class GenreRelation(Relation):
    """{redfm_genre}"""

    arg1: str
    arg2: str

@dataclass
class NamedAfterRelation(Relation):
    """{redfm_named_after}"""

    arg1: str
    arg2: str

@dataclass
class FollowsRelation(Relation):
    """{redfm_follows}"""

    arg1: str
    arg2: str

@dataclass
class HeadquartersLocationRelation(Relation):
    """{redfm_headquarters_location}"""

    arg1: str
    arg2: str

@dataclass
class CastMemberRelation(Relation):
    """{redfm_cast_member}"""

    arg1: str
    arg2: str

@dataclass
class ManufacturerRelation(Relation):
    """{redfm_manufacturer}"""

    arg1: str
    arg2: str

@dataclass
class LocatedInOrNextToBodyOfWaterRelation(Relation):
    """{redfm_located_in_or_next_to_body_of_water}"""

    arg1: str
    arg2: str

@dataclass
class LocationRelation(Relation):
    """{redfm_location}"""

    arg1: str
    arg2: str

@dataclass
class PartOfRelation(Relation):
    """{redfm_part_of}"""

    arg1: str
    arg2: str

@dataclass
class MouthOfTheWatercourseRelation(Relation):
    """{redfm_mouth_of_the_watercourse}"""

    arg1: str
    arg2: str

@dataclass
class MemberOfRelation(Relation):
    """{redfm_member_of}"""

    arg1: str
    arg2: str

@dataclass
class SportRelation(Relation):
    """{redfm_sport}"""

    arg1: str
    arg2: str

@dataclass
class CharactersRelation(Relation):
    """{redfm_characters}"""

    arg1: str
    arg2: str

@dataclass
class ParticipantRelation(Relation):
    """{redfm_participant}"""

    arg1: str
    arg2: str

@dataclass
class NotableWorkRelation(Relation):
    """{redfm_notable_work}"""

    arg1: str
    arg2: str

@dataclass
class ReplacesRelation(Relation):
    """{redfm_replaces}"""

    arg1: str
    arg2: str

@dataclass
class SiblingRelation(Relation):
    """{redfm_sibling}"""

    arg1: str
    arg2: str

@dataclass
class InceptionRelation(Relation):
    """{redfm_inception}"""

    arg1: str
    arg2: str

RELATION_DEFINITIONS: List[Type] = [
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
]

# __all__ = list(map(str, [*ENTITY_DEFINITIONS, *RELATION_DEFINITIONS]))
