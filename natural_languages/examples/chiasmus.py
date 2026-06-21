"""Łowca chiazmów: kwadraty abelowe i palindromy w sekwencjach kolejnych słów.

Skanujemy okna kolejnych słów z Wolnych Lektur (fragment jest więc gramatyczny) i
zbieramy te, których sklejenie jest kwadratem abelowym (struktura lustrzana,
chiazm) lub palindromem. To struktury, w których „sensowne + długie" naprawdę
żyje. Wyniki trafiają do ``results/chiasmus.csv``.

Uruchomienie::

    uv run python -m natural_languages.examples.chiasmus \\
        --books data/wolne_lektury_random_sample_25mb.txt
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from natural_languages.analysis import (
    PhraseMatch,
    is_repetition,
    phrase_abelian_squares,
    phrase_palindromes,
    split_sentences,
)
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


def print_top(title: str, matches: list[PhraseMatch], top: int) -> None:
    """Wypisuje rekord i top-K dopasowań danej struktury."""
    print(f"\n=== {title}: {len(matches)} znalezionych ===")
    if not matches:
        return
    record = matches[0]
    print(f"REKORD: „{record.phrase}” ({record.length} znaków, {len(record.tokens)} słów)")
    for match in matches[:top]:
        tag = " [powtórzenie]" if is_repetition(match.text) else ""
        print(f"  {match.length:>3}  {match.phrase}{tag}")


def write_csv(path: Path, abelian: list[PhraseMatch], palindromes: list[PhraseMatch]) -> None:
    """Zapisuje oba katalogi do jednego CSV z kolumną struktury."""
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["structure", "phrase", "concatenation", "length", "n_tokens"])
        for structure, matches in (("abelian_square", abelian), ("palindrome", palindromes)):
            for match in matches:
                writer.writerow([structure, match.phrase, match.text, match.length, len(match.tokens)])


def main() -> None:
    """Punkt wejścia CLI: szuka chiazmów i palindromów w korpusie, zapisuje CSV."""
    parser = argparse.ArgumentParser(description="Kwadraty abelowe (chiazmy) i palindromy z korpusu.")
    parser.add_argument("--books", "-b", type=Path, required=True, help="Próbka Wolnych Lektur")
    parser.add_argument("--output-dir", "-o", type=Path, default=Path("results"), help="Katalog na CSV")
    parser.add_argument("--max-tokens", type=int, default=16, help="Maks. liczba kolejnych słów w oknie")
    parser.add_argument("--max-length", type=int, default=80, help="Maks. długość sklejenia (znaki)")
    parser.add_argument("--top", type=int, default=20, help="Ile najdłuższych przykładów wypisać")
    args = parser.parse_args()

    preprocessor = TextPreprocessor()
    sentences = tokenize_corpus(args.books, preprocessor)
    print(f"Korpus: {len(sentences)} zdań (>= 2 słowa).")

    abelian = phrase_abelian_squares(sentences, max_tokens=args.max_tokens, max_length=args.max_length)
    palindromes = phrase_palindromes(sentences, max_tokens=args.max_tokens, max_length=args.max_length)

    print_top("Kwadraty abelowe (chiazmy)", abelian, args.top)
    print_top("Palindromy", palindromes, args.top)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / "chiasmus.csv"
    write_csv(out_path, abelian, palindromes)
    print(f"\nZapisano: {out_path}")


if __name__ == "__main__":
    main()
