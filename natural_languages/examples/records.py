"""Rekordy długości: najdłuższe struktury kombinatoryczne w danych.

Szukamy najdłuższych fragmentów struktur w dwóch zakresach:

    - ``słownik`` — wewnątrz pojedynczych słów listy hasłowej,
    - ``korpus`` — przez granice słów w zdaniach z Wolnych Lektur (po usunięciu
      spacji i interpunkcji), czyli np. palindromy typu „kobyła ma mały bok".

Dla słownika liczymy wszystkie cztery struktury (przetasowane kwadraty z limitem
długości). Dla korpusu palindromy liczymy zawsze (Manacher jest liniowy), a
kosztowniejsze kwadraty i kwadraty abelowe tylko dla zdań nie dłuższych niż
``--corpus-max-len`` i dla pierwszych ``--corpus-limit`` zdań. Wyniki trafiają do
``results/records_<lang>.csv``.

Uruchomienie::

    uv run python -m natural_languages.examples.records \\
        --dictionary data/raw/pl.txt --language pl \\
        --books data/wolne_lektury_random_sample_25mb.txt
"""

import argparse
import csv
import os
import sys
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from natural_languages.analysis import (
    Record,
    best_records,
    longest_abelian_square,
    longest_palindrome,
    longest_shuffled_square,
    longest_square,
    split_sentences,
)
from natural_languages.common import StructureType
from natural_languages.data import DataLoader, TextPreprocessor, parse_wolne_lektury_file

LABELS: dict[StructureType, str] = {
    "palindrome": "palindrom",
    "square": "kwadrat (ww)",
    "abelian_square": "kwadrat abelowy",
    "shuffled_square": "przetasowany kwadrat",
}
ORDER: list[StructureType] = ["palindrome", "square", "abelian_square", "shuffled_square"]


def dictionary_records(words: list[str], max_shuffled_len: int) -> dict[StructureType, Record]:
    """Liczy rekordy wszystkich struktur wewnątrz słów listy hasłowej.

    Args:
        words: Znormalizowane słowa.
        max_shuffled_len: Limit długości okna dla przetasowanych kwadratów.

    Returns:
        Mapowanie typ struktury -> rekord.
    """
    finders: dict[StructureType, Callable[[str], str]] = {
        "palindrome": longest_palindrome,
        "square": longest_square,
        "abelian_square": longest_abelian_square,
        "shuffled_square": lambda s: longest_shuffled_square(s, max_length=max_shuffled_len),
    }
    return best_records(words, finders)


def _is_better(record: Record, current: Record | None) -> bool:
    """Czy ``record`` bije ``current``: dłuższy, a przy remisie deterministycznie
    mniejszy leksykograficznie (by wynik nie zależał od kolejności procesów)."""
    if current is None:
        return True
    if record.length != current.length:
        return record.length > current.length
    return (record.match, record.source) < (current.match, current.source)


def _update(best: dict[StructureType, Record], structure: StructureType, match: str, source: str) -> None:
    """Aktualizuje rekord, jeśli nowe dopasowanie jest lepsze (dłuższe lub remis)."""
    if not match:
        return
    candidate = Record(structure, match, source)
    if _is_better(candidate, best.get(structure)):
        best[structure] = candidate


def _scan_chunk(args: tuple[list[str], int]) -> dict[StructureType, Record]:
    """Liczy rekordy korpusu dla jednego kawałka zdań (funkcja workera procesu).

    Funkcja musi być na poziomie modułu, by dało się ją przekazać do
    ``ProcessPoolExecutor`` (pickle). Wewnątrz prowadzi branch-and-bound: po
    znalezieniu długiego kwadratu finderom przekazujemy dolny próg ``min_*``, więc
    pomijamy wszystkie krótsze okresy. Kawałek dostaje zdania uporządkowane malejąco
    długością, więc próg ustala się już na pierwszym (najdłuższym) zdaniu.
    Palindromy (Manacher) liczymy zawsze.

    Args:
        args: Krotka ``(zdania, max_len)`` — kawałek surowych zdań i limit długości
            znormalizowanego zdania dla kwadratów i kwadratów abelowych.

    Returns:
        Najdłuższy rekord każdej struktury w obrębie kawałka.
    """
    sentences, max_len = args
    preprocessor = TextPreprocessor()
    best: dict[StructureType, Record] = {}
    for sentence in sentences:
        normalized = preprocessor.normalize(sentence)
        if len(normalized) < 2:
            continue
        palindrome_floor = best["palindrome"].length + 1 if "palindrome" in best else 2
        _update(best, "palindrome", longest_palindrome(normalized, min_length=palindrome_floor), sentence)
        if len(normalized) <= max_len:
            square_floor = best["square"].length // 2 + 1 if "square" in best else 1
            _update(best, "square", longest_square(normalized, min_period=square_floor), sentence)
            abelian_floor = best["abelian_square"].length // 2 + 1 if "abelian_square" in best else 1
            _update(best, "abelian_square", longest_abelian_square(normalized, min_half=abelian_floor), sentence)
    return best


def merge_records(parts: list[dict[StructureType, Record]]) -> dict[StructureType, Record]:
    """Scala rekordy z wielu kawałków, zostawiając najdłuższy dla każdej struktury."""
    best: dict[StructureType, Record] = {}
    for part in parts:
        for structure, record in part.items():
            if _is_better(record, best.get(structure)):
                best[structure] = record
    return best


def corpus_records(sentences: list[str], max_len: int, limit: int, jobs: int) -> dict[StructureType, Record]:
    """Liczy rekordy przez granice słów w zdaniach korpusu, równolegle.

    Zdania deduplikujemy (poezja i dialogi powtarzają wersy), dzielimy na kawałki
    i przetwarzamy w puli procesów; każdy kawałek prowadzi własny branch-and-bound,
    a wyniki scalamy. Korpus jest „embarrassingly parallel" — praca per zdanie jest
    niezależna.

    Args:
        sentences: Surowe zdania.
        max_len: Maksymalna długość znormalizowanego zdania dla kwadratów.
        limit: Maksymalna liczba unikalnych zdań do przetworzenia.
        jobs: Liczba procesów roboczych (``<= 1`` => sekwencyjnie).

    Returns:
        Mapowanie typ struktury -> rekord (bez przetasowanych kwadratów, zbyt
        kosztownych na poziomie całych zdań).
    """
    unique = list(dict.fromkeys(sentences))[:limit]
    if jobs <= 1 or len(unique) < 2 * jobs:
        return _scan_chunk((unique, max_len))

    # Sortujemy malejąco długością i rozdajemy naprzemiennie (round-robin) do
    # kawałków: każdy kawałek zaczyna od swojego najdłuższego zdania (próg
    # branch-and-bound ustala się natychmiast), a obciążenie jest zbalansowane —
    # drogie, długie zdania trafiają równo do wszystkich procesów.
    ordered = sorted(unique, key=len, reverse=True)
    chunk_count = jobs * 4
    chunks = [(ordered[i::chunk_count], max_len) for i in range(chunk_count)]
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        parts = list(executor.map(_scan_chunk, chunks))
    return merge_records(parts)


def collect_sentences(books_path: Path) -> list[str]:
    """Wczytuje próbkę Wolnych Lektur i dzieli treść utworów na zdania."""
    books = parse_wolne_lektury_file(books_path)
    sentences: list[str] = []
    for book in books:
        sentences.extend(split_sentences(book.text))
    return sentences


def _snippet(text: str, width: int = 80) -> str:
    """Skraca i czyści fragment źródłowy do wypisania/zapisu."""
    collapsed = " ".join(text.split())
    return collapsed if len(collapsed) <= width else collapsed[: width - 1] + "…"


def write_records_csv(path: Path, language: str, scopes: dict[str, dict[StructureType, Record]]) -> None:
    """Zapisuje rekordy do pliku CSV.

    Args:
        path: Ścieżka pliku wyjściowego.
        language: Etykieta języka.
        scopes: Mapowanie nazwa zakresu -> rekordy.
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["language", "scope", "structure", "length", "match", "source"])
        for scope, records in scopes.items():
            for structure in ORDER:
                record = records.get(structure)
                if record is None:
                    continue
                writer.writerow([language, scope, structure, record.length, record.match, _snippet(record.source)])


def print_scope(title: str, records: dict[StructureType, Record]) -> None:
    """Wypisuje tabelę rekordów dla jednego zakresu."""
    print(f"\n=== {title} ===")
    print(f"{'struktura':<22}{'dł.':>5}   przykład")
    print("-" * 70)
    for structure in ORDER:
        record = records.get(structure)
        if record is None:
            print(f"{LABELS[structure]:<22}{'—':>5}")
            continue
        detail = record.match if record.match == record.source else f"{record.match}  ⟵  {_snippet(record.source, 50)}"
        print(f"{LABELS[structure]:<22}{record.length:>5}   {detail}")


def main() -> None:
    """Punkt wejścia CLI: liczy rekordy w słowniku i korpusie, zapisuje CSV."""
    parser = argparse.ArgumentParser(description="Najdłuższe struktury kombinatoryczne w danych.")
    parser.add_argument("--dictionary", "-d", type=Path, required=True, help="Lista słów (jedno na linię)")
    parser.add_argument("--language", "-l", required=True, help="Etykieta języka, np. pl / en")
    parser.add_argument("--books", "-b", type=Path, help="Próbka Wolnych Lektur (opcjonalnie)")
    parser.add_argument("--output-dir", "-o", type=Path, default=Path("results"), help="Katalog na CSV")
    parser.add_argument("--min-length", type=int, default=2, help="Minimalna długość słowa w słowniku")
    parser.add_argument("--max-shuffled-len", type=int, default=40, help="Limit długości dla przetasowanych kwadratów")
    parser.add_argument("--corpus-limit", type=int, default=10_000_000, help="Maks. liczba unikalnych zdań korpusu")
    parser.add_argument("--corpus-max-len", type=int, default=400, help="Maks. długość zdania dla kwadratów (korpus)")
    parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=os.cpu_count() or 1,
        help="Liczba procesów na skan korpusu (domyślnie: rdzenie)",
    )
    args = parser.parse_args()

    preprocessor = TextPreprocessor()
    raw_words = DataLoader(args.dictionary).load_word_list()
    normalized = preprocessor.normalize_words(raw_words)
    words = [w for w in dict.fromkeys(normalized) if len(w) >= args.min_length]
    print(f"Język: {args.language} — {len(words)} unikalnych słów (długość >= {args.min_length}).")

    scopes: dict[str, dict[StructureType, Record]] = {}
    scopes["słownik"] = dictionary_records(words, args.max_shuffled_len)
    print_scope(f"słownik [{args.language}] — najdłuższe struktury wewnątrz słów", scopes["słownik"])

    if args.books:
        if not args.books.exists():
            print(f"\nPominięto korpus — brak pliku {args.books}.")
        else:
            sentences = collect_sentences(args.books)
            print(f"\nKorpus: {len(sentences)} zdań, {args.jobs} proc. (analizuję do {args.corpus_limit} unikalnych).")
            scopes["korpus"] = corpus_records(sentences, args.corpus_max_len, args.corpus_limit, args.jobs)
            print_scope("korpus — najdłuższe struktury przez granice słów", scopes["korpus"])

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / f"records_{args.language}.csv"
    write_records_csv(out_path, args.language, scopes)
    print(f"\nZapisano: {out_path}")


if __name__ == "__main__":
    main()
