from natural_languages.common import StructureMatch


class SquareDetector:
    """Detektor kwadratów i sześcianów w słowach.

    Kwadrat to ciąg postaci ww, gdzie w jest niepustym ciągiem.
    Sześcian to ciąg postaci www.
    Np. 'kankan' = 'kan' + 'kan'.
    """

    def check(self, word: str) -> bool:
        """Sprawdza, czy całe słowo jest kwadratem (postaci ww).

        Args:
            word: Słowo do sprawdzenia.

        Returns:
            True, jeśli słowo ma parzystą, niezerową długość i jego obie połowy
            są identyczne (np. 'kankan').
        """
        n = len(word)
        if n == 0 or n % 2 != 0:
            return False
        half = n // 2
        return word[:half] == word[half:]

    def find(self, word: str) -> list[StructureMatch]:
        """Znajduje wszystkie podciągi będące kwadratami w słowie.

        Args:
            word: Słowo do analizy.

        Returns:
            Lista obiektów StructureMatch dla każdego znalezionego kwadratu.
        """
        results: list[StructureMatch] = []
        n = len(word)
        for i in range(n):
            for length in range(1, (n - i) // 2 + 1):
                half = word[i : i + length]
                if word[i + length : i + 2 * length] == half:
                    results.append(
                        StructureMatch(
                            word=word[i : i + 2 * length],
                            start=i,
                            end=i + 2 * length,
                            structure_type="square",
                            parts=(half, half),
                        )
                    )
        return results

    def find_cubes(self, word: str) -> list[StructureMatch]:
        """Znajduje wszystkie podciągi będące sześcianami w słowie.

        Args:
            word: Słowo do analizy.

        Returns:
            Lista obiektów StructureMatch dla każdego znalezionego sześcianu.
        """
        results: list[StructureMatch] = []
        n = len(word)
        for i in range(n):
            for length in range(1, (n - i) // 3 + 1):
                part = word[i : i + length]
                if word[i + length : i + 2 * length] == part and word[i + 2 * length : i + 3 * length] == part:
                    results.append(
                        StructureMatch(
                            word=word[i : i + 3 * length],
                            start=i,
                            end=i + 3 * length,
                            structure_type="cube",
                            parts=(part, part, part),
                        )
                    )
        return results

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje kwadraty w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Słownik mapujący każde słowo na listę znalezionych kwadratów.
        """
        return {word: self.find(word) for word in words}
