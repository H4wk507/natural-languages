import argparse
from pathlib import Path


class DataLoader:
    """Klasa do ładowania danych wejściowych (listy słów, korpusy tekstowe).

    Args:
        path: Ścieżka do pliku z danymi.
    """

    def __init__(self, path: Path) -> None:
        """Inicjalizuje loader ze ścieżką do pliku.

        Args:
            path: Ścieżka do pliku z danymi.
        """
        self.path = path

    def load_word_list(self) -> list[str]:
        """Ładuje listę słów z pliku tekstowego (jedno słowo na linię).

        Returns:
            Lista słów.
        """
        with open(self.path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def load_corpus(self) -> str:
        """Ładuje korpus tekstowy z pliku.

        Returns:
            Pełna zawartość tekstowa.
        """
        with open(self.path, encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def add_data_args(parser: argparse.ArgumentParser) -> None:
        """Dodaje wspólne argumenty dotyczące danych do parsera argumentów.

        Args:
            parser: Parser argumentów do rozszerzenia.
        """
        parser.add_argument("--input", "-i", type=Path, required=True, help="Ścieżka do pliku wejściowego")
        parser.add_argument(
            "--format",
            choices=["wordlist", "corpus"],
            default="wordlist",
            help="Format danych wejściowych (domyślnie: wordlist)",
        )
        parser.add_argument("--output", "-o", type=Path, help="Ścieżka do pliku wyjściowego CSV")
