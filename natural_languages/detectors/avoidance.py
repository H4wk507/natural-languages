from collections import Counter

from natural_languages.common import StructureMatch


class SquareFreeDetector:
    """Detektor słów bezkwadratowych.

    Słowo bezkwadratowe nie zawiera czynnika postaci xx, gdzie x jest
    niepustym słowem. Thue pokazał w 1906 r., że nad alfabetem 3-literowym
    istnieją dowolnie długie słowa bezkwadratowe; nad alfabetem 2-literowym
    najdłuższe mają długość 3. Konstrukcje te są blisko związane ze słowami
    typu Prouheta-Thuego-Morse'a.
    """

    def check(self, word: str) -> bool:
        """Sprawdza, czy całe słowo jest bezkwadratowe."""
        if not word:
            return False
        return not self._contains_square(word)

    def find(self, word: str) -> list[StructureMatch]:
        """Zwraca całe słowo, jeśli spełnia własność bezkwadratowości."""
        if self.check(word):
            return [
                StructureMatch(
                    word=word,
                    start=0,
                    end=len(word),
                    structure_type="square_free",
                    parts=(word,),
                )
            ]
        return []

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje słowa bezkwadratowe w partii słów."""
        return {word: self.find(word) for word in words}

    @staticmethod
    def _contains_square(word: str) -> bool:
        n = len(word)
        for i in range(n):
            for length in range(1, (n - i) // 2 + 1):
                if word[i : i + length] == word[i + length : i + 2 * length]:
                    return True
        return False


class OverlapFreeDetector:
    """Detektor słów overlap-free.

    Słowo overlap-free nie zawiera czynnika postaci axaxa, gdzie a jest
    pojedynczą literą, a x dowolnym słowem, także pustym.
    """

    def check(self, word: str) -> bool:
        """Sprawdza, czy całe słowo jest overlap-free."""
        if not word:
            return False
        return not self._contains_overlap(word)

    def find(self, word: str) -> list[StructureMatch]:
        """Zwraca całe słowo, jeśli spełnia własność overlap-free."""
        if self.check(word):
            return [
                StructureMatch(
                    word=word,
                    start=0,
                    end=len(word),
                    structure_type="overlap_free",
                    parts=(word,),
                )
            ]
        return []

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje słowa overlap-free w partii słów."""
        return {word: self.find(word) for word in words}

    @staticmethod
    def _contains_overlap(word: str) -> bool:
        n = len(word)
        for i in range(n):
            for block_len in range(1, (n - i + 1) // 2 + 1):
                if i + 2 * block_len >= n:
                    continue
                if word[i : i + block_len] == word[i + block_len : i + 2 * block_len]:
                    if word[i] == word[i + 2 * block_len]:
                        return True
        return False


class AbelianSquareFreeDetector:
    """Detektor słów bezkwadratowych abelowo.

    Słowo jest bezkwadratowe abelowo, jeśli nie zawiera czynnika uv takiego,
    że |u| = |v| oraz u i v mają te same częstości liter.
    """

    def check(self, word: str) -> bool:
        """Sprawdza, czy całe słowo jest bezkwadratowe abelowo."""
        if not word:
            return False
        return not self._contains_abelian_square(word)

    def find(self, word: str) -> list[StructureMatch]:
        """Zwraca całe słowo, jeśli spełnia własność bezkwadratowości abelowej."""
        if self.check(word):
            return [
                StructureMatch(
                    word=word,
                    start=0,
                    end=len(word),
                    structure_type="abelian_square_free",
                    parts=(word,),
                )
            ]
        return []

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje słowa bezkwadratowe abelowo w partii słów."""
        return {word: self.find(word) for word in words}

    @staticmethod
    def _contains_abelian_square(word: str) -> bool:
        n = len(word)
        for i in range(n):
            for half_len in range(1, (n - i) // 2 + 1):
                first = word[i : i + half_len]
                second = word[i + half_len : i + 2 * half_len]
                if Counter(first) == Counter(second):
                    return True
        return False
