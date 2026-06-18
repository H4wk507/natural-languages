from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WolneLekturyBook:
    """Pojedynczy tekst z pliku próbki Wolnych Lektur.

    Attributes:
        title: Tytuł utworu.
        author: Autor utworu.
        slug: Identyfikator lektury w serwisie Wolne Lektury.
        txt_url: Adres pliku TXT w serwisie Wolne Lektury.
        page_url: Adres strony lektury.
        epoch: Epoka literacka.
        kind: Rodzaj literacki.
        genre: Gatunek literacki.
        text: Treść utworu bez nagłówka metadanych.
        metadata: Pełny słownik metadanych z nagłówka.
    """

    title: str
    author: str
    slug: str
    txt_url: str
    page_url: str
    epoch: str
    kind: str
    genre: str
    text: str
    metadata: dict[str, str]


def parse_wolne_lektury_file(path: Path) -> list[WolneLekturyBook]:
    """Parsuje połączony plik tekstów pobranych z Wolnych Lektur.

    Plik powinien składać się z bloków rozpoczynających się od separatora
    ``====`` oraz nagłówka metadanych zawierającego m.in. ``TYTUŁ``, ``AUTOR``,
    ``EPOKA``, ``RODZAJ`` i ``GATUNEK``.

    Args:
        path: Ścieżka do pliku z połączonymi tekstami.

    Returns:
        Lista sparsowanych tekstów wraz z metadanymi.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    books: list[WolneLekturyBook] = []
    index = 0

    while index < len(lines):
        if not _is_book_start(lines, index):
            index += 1
            continue

        metadata, metadata_end = _parse_metadata(lines, index + 1)
        body_start = metadata_end
        if metadata_end < len(lines) and _is_separator(lines[metadata_end]):
            body_start += 1
        body_end = body_start
        while body_end < len(lines) and not _is_book_start(lines, body_end):
            body_end += 1

        books.append(
            WolneLekturyBook(
                title=metadata.get("TYTUŁ", ""),
                author=metadata.get("AUTOR", ""),
                slug=metadata.get("SLUG", ""),
                txt_url=metadata.get("TXT", ""),
                page_url=metadata.get("STRONA", ""),
                epoch=metadata.get("EPOKA", ""),
                kind=metadata.get("RODZAJ", ""),
                genre=metadata.get("GATUNEK", ""),
                text="\n".join(lines[body_start:body_end]).strip(),
                metadata=metadata,
            )
        )
        index = body_end

    return books


def _is_book_start(lines: list[str], index: int) -> bool:
    """Sprawdza, czy dana linia rozpoczyna blok kolejnej lektury."""
    return index + 1 < len(lines) and _is_separator(lines[index]) and lines[index + 1].startswith("TYTUŁ:")


def _is_separator(line: str) -> bool:
    """Rozpoznaje linię separatora złożoną ze znaków ``=``."""
    stripped = line.strip()
    return len(stripped) >= 20 and set(stripped) == {"="}


def _parse_metadata(lines: list[str], start: int) -> tuple[dict[str, str], int]:
    """Czyta metadane od pierwszej linii po separatorze do kolejnego separatora."""
    metadata: dict[str, str] = {}
    index = start
    while index < len(lines) and not _is_separator(lines[index]):
        if ":" in lines[index]:
            key, value = lines[index].split(":", 1)
            metadata[key.strip()] = value.strip()
        index += 1
    return metadata, index


__all__ = ["WolneLekturyBook", "parse_wolne_lektury_file"]
