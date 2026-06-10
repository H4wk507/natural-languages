import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from natural_languages.data import TextPreprocessor
from natural_languages.detectors import (
    AbelianSquareDetector,
    PalindromeDetector,
    SquareDetector,
    TangramDetector,
)


def analyze_word(word: str) -> None:
    """Analizuje pojedyncze słowo pod kątem wszystkich struktur kombinatorycznych.

    Args:
        word: Słowo do analizy.
    """
    preprocessor = TextPreprocessor()
    normalized = preprocessor.normalize(word)
    print(f"Słowo: {word} → znormalizowane: {normalized}")
    print(f"  Długość: {len(normalized)}")

    squares = SquareDetector()
    palindromes = PalindromeDetector(min_length=3)
    abelian = AbelianSquareDetector()
    tangrams = TangramDetector()

    sq = squares.find(normalized)
    if sq:
        print(f"  Kwadraty: {[(m.parts, m.start, m.end) for m in sq]}")

    pal = palindromes.find(normalized)
    if pal:
        print(f"  Palindromy: {[(m.word, m.start, m.end) for m in pal]}")

    ab = abelian.find(normalized)
    if ab:
        print(f"  Kwadraty abelowe: {[(m.parts, m.start, m.end) for m in ab]}")

    tg = tangrams.find(normalized)
    if tg:
        print(f"  Tangram: {[(m.word, m.start, m.end) for m in tg]}")

    print()


def main() -> None:
    """Uruchamia analizę na przykładowych słowach."""
    examples = [
        "kankan",
        "kayak",
        "abracadabra",
        "palindrom",
        "tatar",
        "aabbcc",
        "abcab",
        "aba",
        "abac",
        "abacaba",
    ]
    for word in examples:
        analyze_word(word)


if __name__ == "__main__":
    main()
