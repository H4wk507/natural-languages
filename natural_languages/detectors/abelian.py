from collections import Counter

from natural_languages.common import StructureMatch


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

        Args:
            word: Słowo do analizy.

        Returns:
            Lista obiektów StructureMatch dla każdego kwadratu abelowego.
        """
        results: list[StructureMatch] = []
        n = len(word)
        for i in range(n):
            for half_len in range(1, (n - i) // 2 + 1):
                w1 = word[i : i + half_len]
                w2 = word[i + half_len : i + 2 * half_len]
                if Counter(w1) == Counter(w2):
                    results.append(
                        StructureMatch(
                            word=word[i : i + 2 * half_len],
                            start=i,
                            end=i + 2 * half_len,
                            structure_type="abelian_square",
                            parts=(w1, w2),
                        )
                    )
        return results

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje kwadraty abelowe w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Słownik mapujący każde słowo na listę znalezionych kwadratów abelowych.
        """
        return {word: self.find(word) for word in words}
