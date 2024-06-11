from typing import Dict, List, Type

from ..utils_typing import Entity, dataclass

"""Answer definitions

The answer definitions are derived from the official TydiQA-Gold guidelines:
https://arxiv.org/pdf/2003.05002.pdf
"""


@dataclass
class ShortAnswer(Entity):
    """{tydiqa_shortanswer}"""

    span: str

ANSWER_DEFINITIONS: List[Type] = [
    ShortAnswer
]

# __all__ = list(map(str, [*ANSWER_DEFINITIONS]))
