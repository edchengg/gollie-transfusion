from typing import Dict, List, Type

from src.tasks.redfm.prompts import (
    RELATION_DEFINITIONS,
)
from src.tasks.utils_scorer import EventScorer, RelationScorer, SpanScorer
from src.tasks.utils_typing import Entity, Value

class REDFMRelationScorer(RelationScorer):
    """REDFM Relation identification scorer."""

    valid_types: List[Type] = RELATION_DEFINITIONS