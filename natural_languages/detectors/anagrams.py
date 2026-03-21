from collections import Counter


class AnagramDetector:
    """Detektor anagramów w zbiorach słów.

    Anagramy to słowa o identycznym rozkładzie częstości liter,
    np. 'kot' i 'tok'.
    """

    def check(self, word1: str, word2: str) -> bool:
        """Sprawdza, czy dwa słowa są swoimi anagramami.

        Args:
            word1: Pierwsze słowo.
            word2: Drugie słowo.

        Returns:
            True, jeśli słowa są anagramami.
        """
        return Counter(word1) == Counter(word2)

    def find_groups(self, words: list[str]) -> list[list[str]]:
        """Grupuje słowa będące wzajemnymi anagramami.

        Args:
            words: Lista słów do analizy.

        Returns:
            Lista grup, gdzie każda grupa zawiera słowa będące wzajemnymi anagramami.
            Uwzględniane są tylko grupy z 2+ słowami.
        """
        groups: dict[tuple[tuple[str, int], ...], list[str]] = {}
        for word in words:
            key = tuple(sorted(Counter(word).items()))
            groups.setdefault(key, []).append(word)
        return [group for group in groups.values() if len(group) >= 2]

    def find_all(self, words: list[str]) -> list[list[str]]:
        """Znajduje grupy anagramów w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Lista grup anagramów.
        """
        return self.find_groups(words)
