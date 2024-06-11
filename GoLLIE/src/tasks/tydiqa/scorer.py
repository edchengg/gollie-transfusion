from typing import Dict, List, Type

from src.tasks.tydiqa.prompts import (
    ANSWER_DEFINITIONS,
)
from src.tasks.utils_scorer import QAScorer

class TyDiQAScorer(QAScorer):
    """TydiQA scorer."""

    valid_types: List[Type] = ANSWER_DEFINITIONS