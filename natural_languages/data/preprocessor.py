import re
import unicodedata


class TextPreprocessor:
    """Preprocesor tekstu do analizy kombinatorycznej.

    Obsługuje normalizację, tokenizację i analizę alfabetu.
    Zachowuje znaki diakrytyczne jako osobne symbole (ą ≠ a).
    """

    # Wzorzec dopuszczalnych znaków (litery łacińskie + diakrytyki)
    _LETTER_PATTERN = re.compile(r"[^a-ząćęłńóśźżäöüßàâæçéèêëïîôùûüÿœ]")

    def normalize(self, text: str) -> str:
        """Normalizuje tekst do analizy: małe litery, usunięcie spacji i interpunkcji.

        Args:
            text: Tekst do normalizacji.

        Returns:
            Znormalizowany tekst (małe litery, bez spacji/interpunkcji).
        """
        text = text.lower()
        return self._LETTER_PATTERN.sub("", text)

    def tokenize(self, text: str) -> list[str]:
        """Dzieli tekst na słowa.

        Args:
            text: Tekst do tokenizacji.

        Returns:
            Lista słów (tokeny rozdzielone białymi znakami).
        """
        return text.split()

    def normalize_words(self, words: list[str]) -> list[str]:
        """Normalizuje listę słów.

        Args:
            words: Lista słów do normalizacji.

        Returns:
            Lista znormalizowanych słów (puste ciągi usunięte).
        """
        return [w for w in (self.normalize(word) for word in words) if w]

    def get_alphabet(self, text: str) -> set[str]:
        """Wyodrębnia alfabet (zbiór unikalnych znaków) ze znormalizowanego tekstu.

        Args:
            text: Tekst do analizy (powinien być wcześniej znormalizowany).

        Returns:
            Zbiór unikalnych znaków.
        """
        return set(text)

    @staticmethod
    def char_is_diacritic(char: str) -> bool:
        """Sprawdza, czy znak jest wariantem diakrytycznym (nie zwykłym ASCII).

        Args:
            char: Pojedynczy znak.

        Returns:
            True, jeśli znak zawiera znaki diakrytyczne.
        """
        nfkd = unicodedata.normalize("NFKD", char)
        return len(nfkd) > 1 or (len(char) == 1 and ord(char) > 127)
