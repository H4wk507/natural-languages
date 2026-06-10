from collections import Counter

from natural_languages.common import StructureMatch


class TangramDetector:
    """Detektor tangramów w słowach.

    Tangram to słowo, w którym każda litera występuje parzystą liczbę razy.
    Jest to warunek konieczny bycia przetasowanym kwadratem.
    """

    def check(self, word: str) -> bool:
        """Sprawdza, czy słowo jest tangramem.

        Args:
            word: Słowo do sprawdzenia.

        Returns:
            True, jeśli każda litera występuje parzystą liczbę razy.
        """
        if not word:
            return False
        return all(count % 2 == 0 for count in Counter(word).values())

    def find(self, word: str) -> list[StructureMatch]:
        """Sprawdza, czy całe słowo jest tangramem.

        Args:
            word: Słowo do analizy.

        Returns:
            Lista z jednym StructureMatch, jeśli słowo jest tangramem,
            w przeciwnym razie pusta lista.
        """
        if self.check(word):
            return [
                StructureMatch(
                    word=word,
                    start=0,
                    end=len(word),
                    structure_type="tangram",
                    parts=(word,),
                )
            ]
        return []

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje tangramy w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Słownik mapujący każde słowo na wynik detekcji tangramów.
        """
        return {word: self.find(word) for word in words}
