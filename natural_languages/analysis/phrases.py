"""Struktury w gramatycznych sekwencjach: oknach kolejnych słów z korpusu.

W odróżnieniu od generatywnego sklejania *losowych* słów (``generative.py``), tutaj
szukamy struktur w **kolejnych słowach realnego tekstu** — fragment jest więc
gramatyczny z definicji:

    - przetasowane kwadraty — sensowne frazy oparte na paralelizmie/antytezie
      (np. „zgody lub niezgody humoru lub niehumoru"); naturalny sufit ~34 znaki,
    - kwadraty abelowe — chiazmy/struktury lustrzane (np. „Mgła gęsta, ptak
      czarny… ptak czarny, mgła gęsta"); tu sensowne sekwencje bywają długie,
    - palindromy — frazy typu „kobyła ma mały bok".

Funkcje przyjmują zdania już ztokenizowane (listy znormalizowanych słów) i są
czyste — tokenizację (z preprocesorem danych) wykonuje skrypt eksperymentu.
"""

from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from .records import is_shuffled_square


@dataclass(frozen=True)
class PhraseMatch:
    """Sekwencja kolejnych słów tworząca strukturę po sklejeniu.

    Attributes:
        tokens: Kolejne (znormalizowane) słowa frazy.
    """

    tokens: tuple[str, ...]

    @property
    def text(self) -> str:
        """Sklejenie słów bez spacji (badany napis)."""
        return "".join(self.tokens)

    @property
    def phrase(self) -> str:
        """Fraza ze spacjami (do wyświetlenia)."""
        return " ".join(self.tokens)

    @property
    def length(self) -> int:
        """Długość sklejenia w znakach."""
        return len(self.text)


def is_repetition(text: str) -> bool:
    """Czy napis jest literalnym powtórzeniem (kwadratem ``ww``)."""
    n = len(text)
    return n > 0 and n % 2 == 0 and text[: n // 2] == text[n // 2 :]


def _is_abelian_square(text: str) -> bool:
    """Czy napis jest kwadratem abelowym (parzysta długość, połowy o równym multizbiorze)."""
    n = len(text)
    if n == 0 or n % 2 != 0:
        return False
    mid = n // 2
    return Counter(text[:mid]) == Counter(text[mid:])


def _is_palindrome(text: str) -> bool:
    """Czy napis jest palindromem."""
    return text == text[::-1]


def scan_phrases(
    sentences: Iterable[list[str]],
    predicate: Callable[[str], bool],
    max_tokens: int,
    min_length: int,
    max_length: int,
    exclude_repetitions: bool,
) -> list[PhraseMatch]:
    """Znajduje okna >= 2 kolejnych słów, których sklejenie spełnia ``predicate``.

    Dla każdego zdania przesuwamy okno kolejnych słów, sklejamy je bez spacji i
    testujemy predykatem. Identyczne sklejenia liczymy raz (deduplikacja).

    Args:
        sentences: Zdania jako listy znormalizowanych słów.
        predicate: Test struktury na sklejeniu (np. :func:`is_shuffled_square`).
        max_tokens: Maksymalna liczba kolejnych słów w oknie.
        min_length: Minimalna długość sklejenia.
        max_length: Maksymalna długość sklejenia (zabezpieczenie kosztu).
        exclude_repetitions: Czy pomijać literalne powtórzenia (kwadraty ``ww``).

    Returns:
        Lista dopasowań posortowana malejąco długością, a przy remisie po frazie.
    """
    results: list[PhraseMatch] = []
    seen: set[str] = set()
    for tokens in sentences:
        size = len(tokens)
        for i in range(size):
            concat = ""
            for j in range(i, min(i + max_tokens, size)):
                concat += tokens[j]
                if j == i:
                    continue  # wymagamy co najmniej dwóch słów (sekwencja)
                length = len(concat)
                if length > max_length:
                    break  # dłuższe okna z tego startu też będą za długie
                if length < min_length or concat in seen:
                    continue
                seen.add(concat)
                if exclude_repetitions and is_repetition(concat):
                    continue
                if predicate(concat):
                    results.append(PhraseMatch(tuple(tokens[i : j + 1])))

    results.sort(key=lambda match: (-match.length, match.phrase))
    return results


def phrase_shuffle_squares(
    sentences: Iterable[list[str]],
    max_tokens: int = 6,
    min_length: int = 4,
    max_length: int = 44,
    genuine_only: bool = True,
) -> list[PhraseMatch]:
    """Przetasowane kwadraty w oknach kolejnych słów (domyślnie bez powtórzeń ``ww``)."""
    return scan_phrases(sentences, is_shuffled_square, max_tokens, min_length, max_length, genuine_only)


def phrase_abelian_squares(
    sentences: Iterable[list[str]],
    max_tokens: int = 16,
    min_length: int = 4,
    max_length: int = 80,
    genuine_only: bool = True,
) -> list[PhraseMatch]:
    """Kwadraty abelowe (chiazmy) w oknach kolejnych słów; domyślnie bez powtórzeń ``ww``."""
    return scan_phrases(sentences, _is_abelian_square, max_tokens, min_length, max_length, genuine_only)


def phrase_palindromes(
    sentences: Iterable[list[str]],
    max_tokens: int = 16,
    min_length: int = 4,
    max_length: int = 80,
) -> list[PhraseMatch]:
    """Palindromy w oknach kolejnych słów (np. „kobyła ma mały bok")."""
    return scan_phrases(sentences, _is_palindrome, max_tokens, min_length, max_length, exclude_repetitions=False)
