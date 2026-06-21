"""Wyszukiwanie rekordów: najdłuższych struktur kombinatorycznych w tekście.

W odróżnieniu od detektorów (które pytają „czy CAŁE słowo jest strukturą?"),
ten moduł szuka **najdłuższego fragmentu** danej struktury w pojedynczym ciągu
znaków (token albo znormalizowane zdanie) i jest dobrany pod skalę korpusu:

    - palindrom — algorytm Manachera, ``O(n)``,
    - kwadrat ``ww`` — przeszukiwanie po okresie z wczesnym wyjściem (teoria
      powtórzeń / runs), ``O(n^2)`` w pesymistycznym przypadku, zwykle dużo mniej,
    - kwadrat abelowy — toczące się wektory różnic liczności, ``O(n^2 * sigma)``,
    - przetasowany kwadrat — rozpoznawanie NP-zupełne (Buss, Sołtys 2014); zamiast
      przeglądu ``C(n, n/2)`` podziałów używamy DFS z buforem FIFO i memoizacją,
      poprzedzonego parzystościowym prefiltrem (warunek tangramu).

Funkcje rdzeniowe przyjmują ciąg **już znormalizowany** (małe litery, bez spacji
i interpunkcji) i zwracają najdłuższe dopasowanie jako napis (``""`` gdy brak).
"""

import re
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass

from natural_languages.common import StructureType


def longest_palindrome(s: str, min_length: int = 2) -> str:
    """Znajduje najdłuższy palindromiczny podciąg (algorytm Manachera, ``O(n)``).

    Args:
        s: Znormalizowany ciąg znaków.
        min_length: Minimalna długość zwracanego palindromu.

    Returns:
        Najdłuższy palindrom o długości >= ``min_length`` albo ``""``.
    """
    if len(s) < min_length:
        return ""
    # Transformacja: między znaki i na brzegi wstawiamy strażników, dzięki czemu
    # nie trzeba osobno obsługiwać palindromów parzystej/nieparzystej długości
    # ani granic tablicy ('^' i '$' nigdy nie zrównają się z '#' ani z literą).
    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    radius = [0] * n
    center = right = 0
    for i in range(1, n - 1):
        if i < right:
            radius[i] = min(right - i, radius[2 * center - i])
        while t[i + radius[i] + 1] == t[i - radius[i] - 1]:
            radius[i] += 1
        if i + radius[i] > right:
            center, right = i, i + radius[i]

    best_len = 0
    best_center = 0
    for i in range(1, n - 1):
        if radius[i] > best_len:
            best_len = radius[i]
            best_center = i
    if best_len < min_length:
        return ""
    start = (best_center - best_len) // 2
    return s[start : start + best_len]


def longest_square(s: str, min_period: int = 1) -> str:
    """Znajduje najdłuższy podciąg będący kwadratem ``ww``.

    Kwadrat o okresie ``p`` ma długość ``2p``, więc najdłuższy kwadrat odpowiada
    największemu ``p``, dla którego istnieje pozycja ``i`` z ``s[i:i+p] ==
    s[i+p:i+2p]``. Przeglądamy okresy malejąco i zwracamy pierwsze trafienie.

    Args:
        s: Znormalizowany ciąg znaków.
        min_period: Minimalna długość połowy ``|w|``.

    Returns:
        Najdłuższy kwadrat (napis ``ww``) albo ``""``.
    """
    n = len(s)
    for period in range(n // 2, min_period - 1, -1):
        run = 0
        for i in range(n - period):
            if s[i] == s[i + period]:
                run += 1
                if run >= period:
                    start = i - period + 1
                    return s[start : start + 2 * period]
            else:
                run = 0
    return ""


def _update_diff(diff: dict[str, int], nonzero: int, char: str, delta: int) -> int:
    """Aktualizuje wektor różnic liczności i zwraca nową liczbę niezerowych pozycji."""
    before = diff.get(char, 0)
    after = before + delta
    diff[char] = after
    if before == 0 and after != 0:
        return nonzero + 1
    if before != 0 and after == 0:
        return nonzero - 1
    return nonzero


def longest_abelian_square(s: str, min_half: int = 1) -> str:
    """Znajduje najdłuższy podciąg będący kwadratem abelowym ``w1 w2``.

    ``w1 w2`` jest kwadratem abelowym, gdy ``|w1| = |w2|`` i obie połowy mają ten
    sam multizbiór liter. Dla ustalonej połowy ``L`` przesuwamy dwa sąsiednie okna
    długości ``L`` i utrzymujemy wektor różnic ich liczności w czasie ``O(1)`` na
    krok; połowy przeglądamy malejąco i zwracamy pierwsze trafienie.

    Args:
        s: Znormalizowany ciąg znaków.
        min_half: Minimalna długość połowy ``L``.

    Returns:
        Najdłuższy kwadrat abelowy albo ``""``.
    """
    n = len(s)
    for half in range(n // 2, min_half - 1, -1):
        diff: dict[str, int] = {}
        nonzero = 0
        for k in range(half):
            nonzero = _update_diff(diff, nonzero, s[k], 1)
        for k in range(half, 2 * half):
            nonzero = _update_diff(diff, nonzero, s[k], -1)

        i = 0
        while True:
            if nonzero == 0:
                return s[i : i + 2 * half]
            if i + 2 * half >= n:
                break
            # Okno A traci s[i], zyskuje s[i+half]; okno B (odejmowane) traci
            # s[i+half], zyskuje s[i+2*half].
            nonzero = _update_diff(diff, nonzero, s[i], -1)
            nonzero = _update_diff(diff, nonzero, s[i + half], 1)
            nonzero = _update_diff(diff, nonzero, s[i + half], 1)
            nonzero = _update_diff(diff, nonzero, s[i + 2 * half], -1)
            i += 1
    return ""


def is_shuffled_square(s: str) -> bool:
    """Sprawdza, czy ``s`` jest przetasowanym kwadratem (DFS z buforem FIFO).

    ``s`` jest przetasowanym kwadratem, gdy da się go rozłożyć na dwa rozłączne,
    równe podciągi. Idziemy od lewej i każdą literę przypisujemy do kopii „z
    przodu" (dokładamy do bufora) albo „z tyłu" (musi zgodzić się z początkiem
    bufora — kolejność FIFO, bo obie kopie są tym samym napisem). Sukces, gdy na
    końcu bufor jest pusty. Memoizacja po ``(pozycja, bufor)`` ucina powtórki.

    Rozpoznawanie jest NP-zupełne, więc używać tylko dla krótkich słów. Parzysta
    liczność każdej litery (tangram) to warunek konieczny — sprawdzamy go najpierw.

    Args:
        s: Znormalizowany ciąg znaków.

    Returns:
        True, jeśli ``s`` jest przetasowanym kwadratem.
    """
    n = len(s)
    if n == 0 or n % 2 != 0:
        return False
    if any(count % 2 for count in Counter(s).values()):
        return False

    # present_after[i] = zbiór liter występujących w s[i:]; pozwala w O(1) odrzucić
    # gałąź, w której początku bufora nie da się już domknąć żadną literą z ogona.
    present_after: list[frozenset[str]] = [frozenset()] * (n + 1)
    present: set[str] = set()
    for i in range(n - 1, -1, -1):
        present.add(s[i])
        present_after[i] = frozenset(present)

    seen: set[tuple[int, str]] = set()

    def dfs(i: int, pending: str) -> bool:
        remaining = n - i
        # Bufora dłuższego niż ogon nie da się opróżnić (każda litera zmienia
        # długość bufora o ±1).
        if len(pending) > remaining:
            return False
        # Gdy bufor równy ogonowi, można już tylko domykać: ogon musi być = bufor.
        if len(pending) == remaining:
            return s[i:] == pending
        # Początek bufora musi mieć czym się domknąć w ogonie.
        if pending and pending[0] not in present_after[i]:
            return False
        key = (i, pending)
        if key in seen:
            return False
        seen.add(key)
        char = s[i]
        # Przypisz literę do kopii „z przodu" — wydłuża bufor.
        if dfs(i + 1, pending + char):
            return True
        # Przypisz literę do kopii „z tyłu" — musi domknąć początek bufora.
        if pending and pending[0] == char and dfs(i + 1, pending[1:]):
            return True
        return False

    return dfs(0, "")


def longest_shuffled_square(s: str, max_length: int = 24, min_length: int = 2) -> str:
    """Znajduje najdłuższy podciąg będący przetasowanym kwadratem.

    Rozpoznawanie jest kosztowne, więc okna o nieparzystej liczności litery
    odsiewamy w ``O(1)`` parzystościowym prefiltrem (prefiksowe maski XOR), zanim
    uruchomimy pełny test. Długości przeglądamy malejąco i zwracamy pierwsze
    trafienie. Okna dłuższe niż ``max_length`` są pomijane (zabezpieczenie przed
    wykładniczym kosztem).

    Args:
        s: Znormalizowany ciąg znaków.
        max_length: Górny limit długości badanego okna.
        min_length: Dolny limit długości okna.

    Returns:
        Najdłuższy przetasowany kwadrat albo ``""``.
    """
    n = len(s)
    if n < min_length:
        return ""
    bit: dict[str, int] = {}
    prefix = [0] * (n + 1)
    for i, char in enumerate(s):
        if char not in bit:
            bit[char] = 1 << len(bit)
        prefix[i + 1] = prefix[i] ^ bit[char]

    hi = min(max_length, n)
    if hi % 2:
        hi -= 1
    for length in range(hi, min_length - 1, -2):
        for i in range(n - length + 1):
            if prefix[i + length] != prefix[i]:
                continue  # nieparzysta liczność którejś litery — nie tangram
            window = s[i : i + length]
            if is_shuffled_square(window):
                return window
    return ""


@dataclass(frozen=True)
class Record:
    """Rekordowe (najdłuższe) wystąpienie struktury w zbiorze jednostek.

    Attributes:
        structure_type: Typ struktury.
        match: Najdłuższy znaleziony fragment.
        source: Jednostka (token lub zdanie), w której go znaleziono.
    """

    structure_type: StructureType
    match: str
    source: str

    @property
    def length(self) -> int:
        """Długość rekordowego fragmentu."""
        return len(self.match)


# Domyślny zestaw funkcji rekordowych (jednostka -> najdłuższy fragment).
FINDERS: dict[StructureType, Callable[[str], str]] = {
    "palindrome": longest_palindrome,
    "square": longest_square,
    "abelian_square": longest_abelian_square,
    "shuffled_square": longest_shuffled_square,
}


def best_records(
    units: Iterable[str],
    finders: Mapping[StructureType, Callable[[str], str]] | None = None,
) -> dict[StructureType, Record]:
    """Przegląda jednostki i zapamiętuje najdłuższy fragment każdej struktury.

    Args:
        units: Znormalizowane jednostki (tokeny lub zdania).
        finders: Mapowanie typ struktury -> funkcja rekordowa. Domyślnie
            :data:`FINDERS`.

    Returns:
        Słownik typ struktury -> :class:`Record` z najdłuższym dopasowaniem.
    """
    active = dict(FINDERS) if finders is None else dict(finders)
    best: dict[StructureType, Record] = {}
    for unit in units:
        for structure, finder in active.items():
            match = finder(unit)
            if match and (structure not in best or len(match) > best[structure].length):
                best[structure] = Record(structure, match, unit)
    return best


_SENTENCE_SPLIT = re.compile(r"[.!?…]+")


def split_sentences(text: str) -> list[str]:
    """Dzieli tekst na zdania po znakach ``. ! ? …``.

    Args:
        text: Surowy tekst.

    Returns:
        Lista niepustych (po przycięciu) fragmentów zdaniowych.
    """
    return [part.strip() for part in _SENTENCE_SPLIT.split(text) if part.strip()]
