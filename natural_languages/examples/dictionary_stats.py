"""Statystyki struktur kombinatorycznych w słowniku.

Dla każdego słowa sprawdzamy, czy CAŁE słowo jest:
    - kwadratem ``ww`` (np. kankan),
    - palindromem (np. kajak),
    - kwadratem abelowym (np. kryptoportyk),
    - tangramem,
    - przetasowanym kwadratem (np. prepress),
    - słowem bezkwadratowym,
    - słowem overlap-free,
    - słowem bezkwadratowym abelowo.

Dodatkowo zliczamy grupy anagramów. Wyniki trafiają do dwóch plików CSV
(podsumowanie + katalog trafień), a na ekran wypisywane są rekordy długości.

Uruchomienie::

    uv run python -m natural_languages.examples.dictionary_stats \\
        --input data/raw/pl.txt --language pl
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from natural_languages.data import DataLoader, TextPreprocessor
from natural_languages.detectors import (
    AbelianSquareDetector,
    AbelianSquareFreeDetector,
    AnagramDetector,
    OverlapFreeDetector,
    PalindromeDetector,
    ShuffledSquareDetector,
    SquareDetector,
    SquareFreeDetector,
    TangramDetector,
)

# Kolejność i etykiety badanych struktur (właściwości całego słowa).
STRUCTURES = [
    "square",
    "palindrome",
    "abelian_square",
    "tangram",
    "shuffled_square",
    "square_free",
    "overlap_free",
    "abelian_square_free",
]
LABELS = {
    "square": "kwadrat (ww)",
    "palindrome": "palindrom",
    "abelian_square": "kwadrat abelowy",
    "tangram": "tangram",
    "shuffled_square": "przetasowany kwadrat",
    "square_free": "bezkwadratowe",
    "overlap_free": "overlap-free",
    "abelian_square_free": "bezkwadratowe abelowo",
}


def analyze_words(
    words: list[str], max_shuffled_len: int
) -> tuple[dict[str, int], dict[str, tuple[str, int]], list[tuple[str, int, dict[str, bool]]]]:
    """Sprawdza dla każdego słowa, którymi strukturami jest całe słowo.

    Args:
        words: Lista znormalizowanych słów.
        max_shuffled_len: Maksymalna długość słowa dla (kosztownej) detekcji
            przetasowanych kwadratów. Dłuższe słowa są pomijane w tej kategorii.

    Returns:
        Krotka ``(counts, longest, hits)``:
            - ``counts``: liczba słów w każdej kategorii,
            - ``longest``: najdłuższy przykład (słowo, długość) w każdej kategorii,
            - ``hits``: lista ``(słowo, długość, flagi)`` dla słów pasujących do
              co najmniej jednej struktury.
    """
    square = SquareDetector()
    palindrome = PalindromeDetector()
    abelian = AbelianSquareDetector()
    tangram = TangramDetector()
    shuffled = ShuffledSquareDetector()
    square_free = SquareFreeDetector()
    overlap_free = OverlapFreeDetector()
    abelian_square_free = AbelianSquareFreeDetector()

    counts = dict.fromkeys(STRUCTURES, 0)
    longest: dict[str, tuple[str, int]] = {k: ("", 0) for k in STRUCTURES}
    hits: list[tuple[str, int, dict[str, bool]]] = []

    for word in words:
        n = len(word)
        flags = {
            "square": square.check(word),
            "palindrome": palindrome.check(word),
            "abelian_square": abelian.check(word),
            "tangram": tangram.check(word),
            # Przetasowane kwadraty: detekcja jest wykładnicza, więc ograniczamy
            # długość. Parzystość liter (warunek konieczny) sprawdza sam detektor.
            "shuffled_square": (2 <= n <= max_shuffled_len and n % 2 == 0 and shuffled.check(word)),
            "square_free": square_free.check(word),
            "overlap_free": overlap_free.check(word),
            "abelian_square_free": abelian_square_free.check(word),
        }
        if any(flags.values()):
            hits.append((word, n, flags))
        for key, matched in flags.items():
            if matched:
                counts[key] += 1
                if n > longest[key][1]:
                    longest[key] = (word, n)

    return counts, longest, hits


def top_examples(hits: list[tuple[str, int, dict[str, bool]]], structure: str, k: int) -> list[tuple[str, int]]:
    """Zwraca ``k`` najdłuższych słów pasujących do danej struktury.

    Args:
        hits: Lista trafień z :func:`analyze_words`.
        structure: Nazwa struktury (klucz z :data:`STRUCTURES`).
        k: Maksymalna liczba przykładów.

    Returns:
        Lista ``(słowo, długość)`` posortowana malejąco po długości.
    """
    matched = [(word, n) for (word, n, flags) in hits if flags[structure]]
    matched.sort(key=lambda item: (-item[1], item[0]))
    return matched[:k]


def write_summary_csv(
    path: Path, language: str, n_words: int, counts: dict[str, int], longest: dict[str, tuple[str, int]]
) -> None:
    """Zapisuje podsumowanie statystyk do pliku CSV.

    Args:
        path: Ścieżka pliku wyjściowego.
        language: Etykieta języka.
        n_words: Liczba analizowanych słów.
        counts: Liczność każdej struktury.
        longest: Najdłuższy przykład każdej struktury.
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["language", "n_words", "structure", "count", "pct", "longest_example", "longest_len"])
        for structure in STRUCTURES:
            count = counts[structure]
            pct = 100.0 * count / n_words if n_words else 0.0
            example, length = longest[structure]
            writer.writerow([language, n_words, structure, count, f"{pct:.4f}", example, length])


def write_hits_csv(path: Path, hits: list[tuple[str, int, dict[str, bool]]]) -> None:
    """Zapisuje katalog trafień (słowa pasujące do struktur) do CSV.

    Args:
        path: Ścieżka pliku wyjściowego.
        hits: Lista trafień z :func:`analyze_words`.
    """
    rows = sorted(hits, key=lambda item: (-item[1], item[0]))
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "length", *[f"is_{s}" for s in STRUCTURES]])
        for word, n, flags in rows:
            writer.writerow([word, n, *[int(flags[s]) for s in STRUCTURES]])


def main() -> None:
    """Punkt wejścia CLI: wczytuje słownik, liczy statystyki i zapisuje CSV."""
    parser = argparse.ArgumentParser(description="Statystyki struktur kombinatorycznych w słowniku.")
    parser.add_argument("--input", "-i", type=Path, required=True, help="Plik z listą słów (jedno na linię)")
    parser.add_argument("--language", "-l", required=True, help="Etykieta języka, np. pl / en")
    parser.add_argument("--output-dir", "-o", type=Path, default=Path("results"), help="Katalog na pliki CSV")
    parser.add_argument("--min-length", type=int, default=2, help="Minimalna długość słowa (domyślnie 2)")
    parser.add_argument(
        "--max-shuffled-len",
        type=int,
        default=16,
        help="Maks. długość słowa dla detekcji przetasowanych kwadratów (domyślnie 16)",
    )
    parser.add_argument("--top", type=int, default=15, help="Ile rekordowych przykładów wypisać")
    args = parser.parse_args()

    preprocessor = TextPreprocessor()
    raw_words = DataLoader(args.input).load_word_list()
    normalized = preprocessor.normalize_words(raw_words)
    words = [w for w in dict.fromkeys(normalized) if len(w) >= args.min_length]

    print(f"=== Język: {args.language} ===")
    print(f"Wczytano {len(raw_words)} surowych haseł -> {len(words)} unikalnych słów (długość >= {args.min_length}).\n")

    counts, longest, hits = analyze_words(words, args.max_shuffled_len)
    anagram_groups = AnagramDetector().find_groups(words)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / f"{args.language}_summary.csv"
    hits_path = args.output_dir / f"{args.language}_hits.csv"
    write_summary_csv(summary_path, args.language, len(words), counts, longest)
    write_hits_csv(hits_path, hits)

    n_words = len(words)
    print(f"{'struktura':<22}{'liczba':>10}{'%':>10}   najdłuższy przykład")
    print("-" * 70)
    for structure in STRUCTURES:
        count = counts[structure]
        pct = 100.0 * count / n_words if n_words else 0.0
        example, length = longest[structure]
        print(f"{LABELS[structure]:<22}{count:>10}{pct:>9.3f}%   {example} ({length})")

    print(f"\nRekordy długości (top {args.top}):")
    for structure in STRUCTURES:
        examples = top_examples(hits, structure, args.top)
        shown = ", ".join(f"{w}({n})" for w, n in examples) or "—"
        print(f"  {LABELS[structure]}: {shown}")

    words_in_groups = sum(len(g) for g in anagram_groups)
    print(f"\nAnagramy: {len(anagram_groups)} grup, {words_in_groups} słów w grupach.")
    if anagram_groups:
        largest = max(anagram_groups, key=len)
        print(f"  Największa grupa ({len(largest)}): {', '.join(sorted(largest)[:12])}")

    print(f"\nZapisano: {summary_path} oraz {hits_path}")


if __name__ == "__main__":
    main()
