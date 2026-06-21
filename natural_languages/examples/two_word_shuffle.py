"""Dwuwyrazowe przetasowane kwadraty: rekordy ze sklejeń słów słownika.

Pojedyncze słowa rzadko są tangramami, więc najdłuższe przetasowane kwadraty
powstają dopiero ze sklejenia dwóch różnych słów ``w1 + w2``. Dzięki kubełkom
parzystości (oba słowa muszą mieć tę samą maskę parzystości, by sklejenie było
tangramem) testujemy tylko ułamek wszystkich par. Wyniki trafiają do
``results/two_word_shuffle_<lang>.csv``.

Uruchomienie::

    uv run python -m natural_languages.examples.two_word_shuffle \\
        --dictionary data/raw/pl.txt --language pl
"""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from natural_languages.analysis import WordPair, two_word_shuffles
from natural_languages.data import DataLoader, TextPreprocessor


def is_anagram_pair(pair: WordPair) -> bool:
    """Czy słowa pary są anagramami (ten sam multizbiór liter)."""
    return Counter(pair.first) == Counter(pair.second)


def write_pairs_csv(path: Path, language: str, pairs: list[WordPair]) -> None:
    """Zapisuje katalog par do CSV.

    Args:
        path: Ścieżka pliku wyjściowego.
        language: Etykieta języka.
        pairs: Pary posortowane malejąco długością.
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["language", "first", "second", "concatenation", "length", "is_anagram"])
        for pair in pairs:
            writer.writerow([language, pair.first, pair.second, pair.text, pair.length, int(is_anagram_pair(pair))])


def main() -> None:
    """Punkt wejścia CLI: szuka dwuwyrazowych przetasowanych kwadratów, zapisuje CSV."""
    parser = argparse.ArgumentParser(description="Dwuwyrazowe przetasowane kwadraty ze słownika.")
    parser.add_argument("--dictionary", "-d", type=Path, required=True, help="Lista słów (jedno na linię)")
    parser.add_argument("--language", "-l", required=True, help="Etykieta języka, np. pl / en")
    parser.add_argument("--output-dir", "-o", type=Path, default=Path("results"), help="Katalog na CSV")
    parser.add_argument("--min-word-len", type=int, default=2, help="Minimalna długość słowa wejściowego")
    parser.add_argument("--max-pair-len", type=int, default=None, help="Maks. długość sklejenia (domyślnie bez limitu)")
    parser.add_argument("--top", type=int, default=25, help="Ile najdłuższych przykładów wypisać")
    args = parser.parse_args()

    preprocessor = TextPreprocessor()
    raw_words = DataLoader(args.dictionary).load_word_list()
    normalized = preprocessor.normalize_words(raw_words)
    words = [w for w in dict.fromkeys(normalized) if len(w) >= args.min_word_len]
    print(f"Język: {args.language} — {len(words)} unikalnych słów (długość >= {args.min_word_len}).")

    pairs = two_word_shuffles(words, max_length=args.max_pair_len)
    anagram_count = sum(is_anagram_pair(p) for p in pairs)
    print(f"Dwuwyrazowych przetasowanych kwadratów: {len(pairs)} "
          f"(w tym {anagram_count} z par anagramów, {len(pairs) - anagram_count} z par nieanagramowych).")

    if pairs:
        record = pairs[0]
        print(f"\nREKORD: {record.first} + {record.second} = {record.text} ({record.length} liter)")
        print(f"\nTop {args.top} najdłuższych:")
        for pair in pairs[: args.top]:
            tag = " [anagramy]" if is_anagram_pair(pair) else ""
            print(f"  {pair.length:>2}  {pair.first} + {pair.second}  ->  {pair.text}{tag}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / f"two_word_shuffle_{args.language}.csv"
    write_pairs_csv(out_path, args.language, pairs)
    print(f"\nZapisano: {out_path}")


if __name__ == "__main__":
    main()
