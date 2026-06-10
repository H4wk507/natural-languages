from itertools import combinations

from natural_languages.common import StructureMatch

from .tangrams import TangramDetector


class ShuffledSquareDetector:
    """Detektor przetasowanych kwadratów w słowach.

    Przetasowany kwadrat to słowo, które można rozłożyć na dwa identyczne
    podciągi. Np. 'abab' można podzielić na podciągi 'ab' (pozycje 0,1)
    i 'ab' (pozycje 2,3).
    """

    MAX_WORD_LENGTH = 20

    def check(self, word: str) -> bool:
        """Sprawdza, czy słowo jest przetasowanym kwadratem.

        Args:
            word: Słowo do sprawdzenia.

        Returns:
            True, jeśli słowo jest przetasowanym kwadratem.

        Raises:
            ValueError: Jeśli słowo przekracza MAX_WORD_LENGTH znaków.
        """
        n = len(word)
        if n % 2 != 0 or n == 0:
            return False
        if n > self.MAX_WORD_LENGTH:
            raise ValueError(
                f"Długość słowa {n} przekracza maksimum {self.MAX_WORD_LENGTH} dla detekcji przetasowanych kwadratów"
            )

        if not TangramDetector().check(word):
            return False

        half = n // 2

        # Sprawdzamy wszystkie podzbiory indeksów rozmiaru half
        # Dla n <= 20 to najwyżej C(20,10) = 184756 — wykonalne
        for indices in combinations(range(n), half):
            idx_set = set(indices)
            subseq1 = "".join(word[k] for k in indices)
            subseq2 = "".join(word[k] for k in range(n) if k not in idx_set)
            if subseq1 == subseq2:
                return True
        return False

    def find(self, word: str) -> list[StructureMatch]:
        """Sprawdza, czy całe słowo jest przetasowanym kwadratem.

        Args:
            word: Słowo do analizy (maks. MAX_WORD_LENGTH znaków).

        Returns:
            Lista z jednym StructureMatch, jeśli słowo jest przetasowanym kwadratem,
            w przeciwnym razie pusta lista.
        """
        if len(word) > self.MAX_WORD_LENGTH:
            return []
        if self.check(word):
            return [
                StructureMatch(
                    word=word,
                    start=0,
                    end=len(word),
                    structure_type="shuffled_square",
                    parts=(word,),
                )
            ]
        return []

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje przetasowane kwadraty w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Słownik mapujący każde słowo na wyniki detekcji przetasowanych kwadratów.
        """
        return {word: self.find(word) for word in words if len(word) <= self.MAX_WORD_LENGTH}
