from typing import Dict, List, Type

from src.tasks.conll04.prompts import (
    RELATION_DEFINITIONS,
)
from src.tasks.utils_scorer import EventScorer, RelationScorer, SpanScorer
from src.tasks.utils_typing import Entity, Value

class CoNLL04RelationScorer(RelationScorer):
    """CoNLL04 Relation identification scorer."""

    valid_types: List[Type] = RELATION_DEFINITIONS