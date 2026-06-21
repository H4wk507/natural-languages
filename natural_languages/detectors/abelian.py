from collections import Counter

from natural_languages.common import StructureMatch


def _apply_delta(diff: dict[str, int], nonzero: int, char: str, delta: int) -> int:
    """Aktualizuje wektor różnic liczności i zwraca nową liczbę niezerowych pozycji.

    Args:
        diff: Wektor różnic ``freq(w1) - freq(w2)`` (modyfikowany w miejscu).
        nonzero: Aktualna liczba liter o niezerowej różnicy.
        char: Litera, której różnicę zmieniamy.
        delta: Zmiana różnicy (zwykle +1 lub -1).

    Returns:
        Zaktualizowana liczba liter o niezerowej różnicy.
    """
    before = diff.get(char, 0)
    after = before + delta
    diff[char] = after
    if before == 0 and after != 0:
        return nonzero + 1
    if before != 0 and after == 0:
        return nonzero - 1
    return nonzero


class AbelianSquareDetector:
    """Detektor kwadratów abelowych w słowach.

    Kwadrat abelowy to ciąg w1w2, gdzie |w1| = |w2| i w2 jest
    anagramem w1 (tj. mają te same częstości liter).
    """

    def check(self, word: str) -> bool:
        """Sprawdza, czy słowo jest kwadratem abelowym.

        Args:
            word: Słowo do sprawdzenia (musi mieć parzystą długość).

        Returns:
            True, jeśli słowo jest kwadratem abelowym.
        """
        n = len(word)
        if n % 2 != 0 or n == 0:
            return False
        mid = n // 2
        return Counter(word[:mid]) == Counter(word[mid:])

    def find(self, word: str) -> list[StructureMatch]:
        """Znajduje wszystkie podciągi będące kwadratami abelowymi w słowie.

        Dla ustalonej długości połowy ``L`` przesuwamy dwa sąsiednie okna długości
        ``L`` i utrzymujemy wektor różnic ich liczności, aktualizowany w O(1) na
        krok — zamiast budować nowe ``Counter`` dla każdego podciągu. Łącznie
        O(n^2) zamiast O(n^3).

        Args:
            word: Słowo do analizy.

        Returns:
            Lista obiektów StructureMatch dla każdego kwadratu abelowego,
            uporządkowana rosnąco po (start, end).
        """
        results: list[StructureMatch] = []
        n = len(word)
        for half in range(1, n // 2 + 1):
            diff: dict[str, int] = {}
            nonzero = 0
            for k in range(half):
                nonzero = _apply_delta(diff, nonzero, word[k], 1)
            for k in range(half, 2 * half):
                nonzero = _apply_delta(diff, nonzero, word[k], -1)

            i = 0
            while True:
                if nonzero == 0:
                    results.append(
                        StructureMatch(
                            word=word[i : i + 2 * half],
                            start=i,
                            end=i + 2 * half,
                            structure_type="abelian_square",
                            parts=(word[i : i + half], word[i + half : i + 2 * half]),
                        )
                    )
                if i + 2 * half >= n:
                    break
                # Okno w1 traci word[i], zyskuje word[i+half]; okno w2 (odejmowane)
                # traci word[i+half], zyskuje word[i+2*half].
                nonzero = _apply_delta(diff, nonzero, word[i], -1)
                nonzero = _apply_delta(diff, nonzero, word[i + half], 1)
                nonzero = _apply_delta(diff, nonzero, word[i + half], 1)
                nonzero = _apply_delta(diff, nonzero, word[i + 2 * half], -1)
                i += 1

        results.sort(key=lambda match: (match.start, match.end))
        return results

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje kwadraty abelowe w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Słownik mapujący każde słowo na listę znalezionych kwadratów abelowych.
        """
        return {word: self.find(word) for word in words}
