from natural_languages.common import StructureMatch


class PalindromeDetector:
    """Detektor palindromów w słowach.

    Palindrom to słowo równe swojemu odwróceniu, np. 'kajak'.
    """

    def __init__(self, min_length: int = 2) -> None:
        """Inicjalizuje detektor palindromów.

        Args:
            min_length: Minimalna długość palindromów do zgłoszenia.
        """
        self.min_length = min_length

    def check(self, word: str) -> bool:
        """Sprawdza, czy słowo jest palindromem.

        Args:
            word: Słowo do sprawdzenia.

        Returns:
            True, jeśli słowo jest palindromem.
        """
        return word == word[::-1]

    def find(self, word: str) -> list[StructureMatch]:
        """Znajduje wszystkie palindromiczne podciągi w słowie.

        Args:
            word: Słowo do analizy.

        Returns:
            Lista obiektów StructureMatch dla każdego palindromu.
        """
        results: list[StructureMatch] = []
        n = len(word)
        for i in range(n):
            for j in range(i + self.min_length, n + 1):
                sub = word[i:j]
                if sub == sub[::-1]:
                    results.append(
                        StructureMatch(
                            word=sub,
                            start=i,
                            end=j,
                            structure_type="palindrome",
                            parts=(sub,),
                        )
                    )
        return results

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje palindromy w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Słownik mapujący każde słowo na listę znalezionych palindromów.
        """
        return {word: self.find(word) for word in words}
