from typing import Dict, List, Type

from ..utils_typing import Entity, dataclass


class Scientist(Entity):
    """{multiconer_scientist}"""

    span: str # {multiconer_scientist_examples}

class Artist(Entity):
    """{multiconer_artist}"""

    span: str # {multiconer_artist_examples}

class Athlete(Entity):
    """{multiconer_athlete}"""

    span: str # {multiconer_athlete_examples}

class Politician(Entity):
    """{multiconer_politician}"""

    span: str # {multiconer_politician_examples}

class Cleric(Entity):
    """{multiconer_cleric}"""

    span: str # {multiconer_cleric_examples}

class SportsManager(Entity):
    """{multiconer_sports_manager}"""

    span: str # {multiconer_sports_manager_examples}

class OtherPerson(Entity):
    """{multiconer_other_person}"""

    span: str # {multiconer_other_person_examples}

class MusicalGroup(Entity):
    """{multiconer_musical_group}"""

    span: str # {multiconer_musical_group_examples}

class PublicCorp(Entity):
    """{multiconer_public_corp}"""
    span: str # {multiconer_public_corp_examples}

class PrivateCorp(Entity):
    """{multiconer_private_corp}"""

    span: str # {multiconer_private_corp_examples}

class AerospaceManufacturer(Entity):
    """{multiconer_aerospace_manufacturer}"""

    span: str # {multiconer_aerospace_manufacturer_examples}

class SportsGroup(Entity):
    """{multiconer_sports_group}"""

    span: str # {multiconer_sports_group_examples}

class OtherGroup(Entity):
    """{multiconer_other_group}"""

    span: str # {multiconer_other_group_examples}

class VisualWork(Entity):
    """{multiconer_visual_work}"""

    span: str # {multiconer_visual_work_examples}

class MusicalWork(Entity):
    """{multiconer_musical_work}"""

    span: str # {multiconer_musical_work_examples}

class WrittenWork(Entity):
    """{multiconer_written_work}"""

    span: str # {multiconer_written_work_examples}

class ArtWork(Entity):
    """{multiconer_art_work}"""

    span: str # {multiconer_art_work_examples}

class Software(Entity):
    """{multiconer_software}"""

    span: str # {multiconer_software_examples}

class Facility(Entity):
    """{multiconer_facility}"""

    span: str # {multiconer_facility_examples}

class HumanSettlement(Entity):
    """{multiconer_human_settlement}"""

    span: str # {multiconer_human_settlement_examples}

class Station(Entity):
    """{multiconer_station}"""

    span: str # {multiconer_station_examples}

class OtherLocation(Entity):
    """{multiconer_other_location}"""

    span: str # {multiconer_other_location_examples}

class Clothing(Entity):
    """{multiconer_clothing}"""

    span: str # {multiconer_clothing_examples}

class Vehicle(Entity):
    """{multiconer_vehicle}"""

    span: str # {multiconer_vehicle_examples}

class Food(Entity):
    """{multiconer_food}"""

    span: str # {multiconer_food_examples}

class Drink(Entity):
    """{multiconer_drink}"""

    span: str # {multiconer_drink_examples}

class OtherProduct(Entity):
    """{multiconer_other_product}"""

    span: str # {multiconer_other_product_examples}

class MedicationOrVaccine(Entity):
    """{multiconer_medication_or_vaccine}"""

    span: str # {multiconer_medication_or_vaccine_examples}

class MedicalProcedure(Entity):
    """{multiconer_medical_procedure}"""

    span: str # {multiconer_medical_procedure_examples}

class AnatomicalStructure(Entity):
    """{multiconer_anatomical_structure}"""

    span: str # {multiconer_anatomical_structure_examples}

class Symptom(Entity):
    """{multiconer_symtpom}"""

    span: str # {multiconer_symptom_examples}

class Disease(Entity):
    """{multiconer_disease}"""

    span: str # {multiconer_disease_examples}

ENTITY_DEFINITIONS: List[Type] = [
    Scientist,
    Artist,
    Athlete,
    Politician,
    Cleric,
    SportsManager,
    OtherPerson,
    MusicalGroup,
    PublicCorp,
    PrivateCorp,
    AerospaceManufacturer,
    SportsGroup,
    OtherGroup,
    VisualWork,
    MusicalWork,
    WrittenWork,
    ArtWork,
    Software,
    Facility,
    HumanSettlement,
    Station,
    OtherLocation,
    Clothing,
    Vehicle,
    Food,
    Drink,
    OtherProduct,
    MedicationOrVaccine,
    MedicalProcedure,
    AnatomicalStructure,
    Symptom,
    Disease,
]
