"""Gramatyczne przetasowane kwadraty: sensowne sekwencje kolejnych słów z korpusu.

Skanujemy okna kolejnych słów z Wolnych Lektur (fragment jest więc gramatyczny) i
zbieramy te, których sklejenie jest przetasowanym kwadratem. Domyślnie pomijamy
literalne powtórzenia (``ww``) — interesują nas genuine przeplecenia, zwykle oparte
na paralelizmie/antytezie. Wyniki trafiają do ``results/grammatical_shuffle.csv``.

Uruchomienie::

    uv run python -m natural_languages.examples.grammatical_shuffle \\
        --books data/wolne_lektury_random_sample_25mb.txt
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from natural_languages.analysis import PhraseMatch, is_repetition, phrase_shuffle_squares, split_sentences
from natural_languages.data import TextPreprocessor, parse_wolne_lektury_file


def tokenize_corpus(books_path: Path, preprocessor: TextPreprocessor) -> list[list[str]]:
    """Wczytuje korpus i zwraca zdania jako listy znormalizowanych słów."""
    sentences: list[list[str]] = []
    for book in parse_wolne_lektury_file(books_path):
        for sentence in split_sentences(book.text):
            tokens = [token for token in (preprocessor.normalize(word) for word in sentence.split()) if token]
            if len(tokens) >= 2:
                sentences.append(tokens)
    return sentences


def write_phrases_csv(path: Path, matches: list[PhraseMatch]) -> None:
    """Zapisuje katalog fraz do CSV."""
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["phrase", "concatenation", "length", "n_tokens"])
        for match in matches:
            writer.writerow([match.phrase, match.text, match.length, len(match.tokens)])


def main() -> None:
    """Punkt wejścia CLI: szuka gramatycznych przetasowanych kwadratów, zapisuje CSV."""
    parser = argparse.ArgumentParser(description="Gramatyczne przetasowane kwadraty z korpusu.")
    parser.add_argument("--books", "-b", type=Path, required=True, help="Próbka Wolnych Lektur")
    parser.add_argument("--output-dir", "-o", type=Path, default=Path("results"), help="Katalog na CSV")
    parser.add_argument("--max-tokens", type=int, default=6, help="Maks. liczba kolejnych słów w oknie")
    parser.add_argument("--max-length", type=int, default=44, help="Maks. długość sklejenia (znaki)")
    parser.add_argument("--top", type=int, default=25, help="Ile najdłuższych przykładów wypisać")
    parser.add_argument(
        "--include-repetitions", action="store_true", help="Nie pomijaj literalnych powtórzeń (ww)"
    )
    args = parser.parse_args()

    preprocessor = TextPreprocessor()
    sentences = tokenize_corpus(args.books, preprocessor)
    print(f"Korpus: {len(sentences)} zdań (>= 2 słowa).")

    matches = phrase_shuffle_squares(
        sentences,
        max_tokens=args.max_tokens,
        max_length=args.max_length,
        genuine_only=not args.include_repetitions,
    )
    kind = "wszystkich" if args.include_repetitions else "genuine (bez powtórzeń)"
    print(f"Gramatycznych przetasowanych kwadratów ({kind}): {len(matches)}.")

    if matches:
        record = matches[0]
        print(f'\nREKORD: „{record.phrase}” ({record.length} znaków, {len(record.tokens)} słów)')
        print(f"\nTop {args.top} najdłuższych:")
        for match in matches[: args.top]:
            tag = " [powtórzenie]" if is_repetition(match.text) else ""
            print(f"  {match.length:>2}  {match.phrase}{tag}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / "grammatical_shuffle.csv"
    write_phrases_csv(out_path, matches)
    print(f"\nZapisano: {out_path}")


if __name__ == "__main__":
    main()
