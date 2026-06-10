from .abelian import AbelianSquareDetector
from .anagrams import AnagramDetector
from .avoidance import AbelianSquareFreeDetector, OverlapFreeDetector, SquareFreeDetector
from .palindromes import PalindromeDetector
from .shuffled import ShuffledSquareDetector
from .squares import SquareDetector
from .tangrams import TangramDetector

__all__ = [
    "AbelianSquareDetector",
    "AbelianSquareFreeDetector",
    "AnagramDetector",
    "OverlapFreeDetector",
    "PalindromeDetector",
    "ShuffledSquareDetector",
    "SquareDetector",
    "SquareFreeDetector",
    "TangramDetector",
]
