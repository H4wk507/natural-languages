from dataclasses import dataclass
from typing import Literal

StructureType = Literal[
    "square",
    "cube",
    "palindrome",
    "abelian_square",
    "shuffled_square",
    "tangram",
]


@dataclass(frozen=True)
class StructureMatch:
    """Wykryta struktura kombinatoryczna w słowie lub frazie.

    Attributes:
        word: Oryginalne słowo lub fraza.
        start: Indeks początkowy dopasowania.
        end: Indeks końcowy dopasowania (wyłącznie).
        structure_type: Typ struktury.
        parts: Rozłożone części struktury.
    """

    word: str
    start: int
    end: int
    structure_type: StructureType
    parts: tuple[str, ...]
