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

    @staticmethod
    def _palindrome_radii(word: str) -> list[int]:
        """Liczy promienie palindromów algorytmem Manachera w czasie O(n).

        Na ciągu z wstawionymi strażnikami ``^#...#$`` (między znaki i na brzegi)
        promień w danym centrum jest równy długości najdłuższego palindromu w
        oryginalnym słowie o tym centrum — bez osobnej obsługi długości parzystych
        i nieparzystych.

        Args:
            word: Słowo do analizy.

        Returns:
            Tablica promieni indeksowana centrami ciągu z strażnikami.
        """
        t = "^#" + "#".join(word) + "#$"
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
        return radius

    def find(self, word: str) -> list[StructureMatch]:
        """Znajduje wszystkie palindromiczne podciągi w słowie.

        Promienie liczymy raz algorytmem Manachera (O(n)), a następnie z każdego
        centrum odtwarzamy wszystkie palindromy (kurcząc od najdłuższego co 2 znaki).
        Łącznie O(n + liczba palindromów) — zamiast O(n^3) jak naiwne porównywanie
        każdego podciągu z jego odwróceniem.

        Args:
            word: Słowo do analizy.

        Returns:
            Lista obiektów StructureMatch dla każdego palindromu, uporządkowana
            rosnąco po (start, end).
        """
        results: list[StructureMatch] = []
        if len(word) < self.min_length:
            return results
        radius = self._palindrome_radii(word)
        for center in range(1, len(radius) - 1):
            for length in range(radius[center], self.min_length - 1, -2):
                start = (center - length) // 2
                sub = word[start : start + length]
                results.append(
                    StructureMatch(
                        word=sub,
                        start=start,
                        end=start + length,
                        structure_type="palindrome",
                        parts=(sub,),
                    )
                )
        results.sort(key=lambda match: (match.start, match.end))
        return results

    def find_all(self, words: list[str]) -> dict[str, list[StructureMatch]]:
        """Znajduje palindromy w partii słów.

        Args:
            words: Lista słów do analizy.

        Returns:
            Słownik mapujący każde słowo na listę znalezionych palindromów.
        """
        return {word: self.find(word) for word in words}
