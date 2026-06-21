"""Generatywne szukanie struktur powstających ze sklejenia dwóch słów.

Najciekawszy przypadek to **dwuwyrazowe przetasowane kwadraty**: pary różnych słów
``w1, w2``, dla których ``w1 + w2`` jest przetasowanym kwadratem (rozkłada się na
dwa równe podciągi). Pojedyncze słowa rzadko bywają tangramami, więc rekordy
przetasowanych kwadratów „mieszkają" właśnie w sklejeniach — to wątek z artykułu
B. Pawlika i pracy L. Mola.

Klucz do wydajności to **kubełki parzystości**. Przetasowany kwadrat musi być
tangramem (każda litera parzyście), a dla sklejenia:

    parity(w1 + w2) = parity(w1) XOR parity(w2),

gdzie ``parity(w)`` to maska bitowa liter występujących nieparzyście. Sklejenie
jest tangramem wtedy i tylko wtedy, gdy ``parity(w1) == parity(w2)``. Wystarczy
więc grupować słowa po masce parzystości i testować tylko pary w obrębie kubełka —
dla słownika PL to ~443 tys. par zamiast ~10^11 wszystkich.
"""

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from .records import is_shuffled_square


@dataclass(frozen=True)
class WordPair:
    """Para słów, których sklejenie tworzy strukturę.

    Attributes:
        first: Pierwsze słowo.
        second: Drugie słowo.
    """

    first: str
    second: str

    @property
    def text(self) -> str:
        """Sklejenie ``first + second``."""
        return self.first + self.second

    @property
    def length(self) -> int:
        """Długość sklejenia."""
        return len(self.first) + len(self.second)


def build_bit_index(words: Iterable[str]) -> dict[str, int]:
    """Buduje spójne mapowanie litera -> bit, wspólne dla wszystkich słów.

    Args:
        words: Słowa, z których wyznaczamy alfabet.

    Returns:
        Mapowanie każdej litery na unikalny bit (potęgę dwójki).
    """
    alphabet = sorted({ch for word in words for ch in word})
    return {ch: 1 << index for index, ch in enumerate(alphabet)}


def parity_mask(word: str, bit_index: dict[str, int]) -> int:
    """Wyznacza maskę parzystości: bit litery zapalony, gdy występuje nieparzyście.

    Args:
        word: Słowo.
        bit_index: Mapowanie litera -> bit z :func:`build_bit_index`.

    Returns:
        Maska bitowa parzystości liter słowa.
    """
    mask = 0
    for ch in word:
        mask ^= bit_index[ch]
    return mask


def bucket_by_parity(words: list[str], bit_index: dict[str, int]) -> dict[int, list[str]]:
    """Grupuje słowa po masce parzystości.

    Args:
        words: Lista słów.
        bit_index: Mapowanie litera -> bit z :func:`build_bit_index`.

    Returns:
        Mapowanie maska parzystości -> lista słów o tej masce.
    """
    buckets: defaultdict[int, list[str]] = defaultdict(list)
    for word in words:
        buckets[parity_mask(word, bit_index)].append(word)
    return dict(buckets)


def two_word_shuffles(words: Iterable[str], min_length: int = 2, max_length: int | None = None) -> list[WordPair]:
    """Znajduje wszystkie pary różnych słów, których sklejenie jest przetasowanym kwadratem.

    Sklejenie musi być tangramem, więc testujemy tylko pary o tej samej masce
    parzystości (oba uporządkowania ``w1+w2`` i ``w2+w1`` traktujemy osobno, bo to
    różne napisy). Sklejenia identycznych słów pomijamy — ``ww`` jest kwadratem
    trywialnie.

    Args:
        words: Słowa do sparowania (duplikaty są usuwane).
        min_length: Minimalna długość sklejenia.
        max_length: Maksymalna długość sklejenia (zabezpieczenie kosztu); ``None``
            oznacza brak limitu.

    Returns:
        Lista par posortowana malejąco długością, a przy remisie leksykograficznie
        (deterministycznie).
    """
    unique = list(dict.fromkeys(words))
    bit_index = build_bit_index(unique)
    buckets = bucket_by_parity(unique, bit_index)

    results: list[WordPair] = []
    for group in buckets.values():
        size = len(group)
        if size < 2:
            continue
        for i in range(size):
            for j in range(size):
                if i == j:
                    continue
                total = len(group[i]) + len(group[j])
                if total < min_length or (max_length is not None and total > max_length):
                    continue
                if is_shuffled_square(group[i] + group[j]):
                    results.append(WordPair(group[i], group[j]))

    results.sort(key=lambda pair: (-pair.length, pair.text))
    return results
