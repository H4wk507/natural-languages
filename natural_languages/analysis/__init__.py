from .generative import (
    WordPair,
    bucket_by_parity,
    build_bit_index,
    parity_mask,
    two_word_shuffles,
)
from .phrases import (
    PhraseMatch,
    is_repetition,
    phrase_abelian_squares,
    phrase_palindromes,
    phrase_shuffle_squares,
    scan_phrases,
)
from .records import (
    FINDERS,
    Record,
    best_records,
    is_shuffled_square,
    longest_abelian_square,
    longest_palindrome,
    longest_shuffled_square,
    longest_square,
    split_sentences,
)

__all__ = [
    "FINDERS",
    "PhraseMatch",
    "Record",
    "WordPair",
    "best_records",
    "bucket_by_parity",
    "build_bit_index",
    "is_repetition",
    "is_shuffled_square",
    "longest_abelian_square",
    "longest_palindrome",
    "longest_shuffled_square",
    "longest_square",
    "parity_mask",
    "phrase_abelian_squares",
    "phrase_palindromes",
    "phrase_shuffle_squares",
    "scan_phrases",
    "split_sentences",
    "two_word_shuffles",
]
