"""Pobieranie i przygotowanie list słów do eksperymentów.

Słowniki pochodzą z hunspell LibreOffice i są pobierane przez HTTPS, więc skrypt
działa niezależnie od systemu operacyjnego (cross-platform — nie korzysta z
lokalnych słowników typu ``/usr/share/dict/words``):

    - angielski: ``en_US`` (kodowanie UTF-8),
    - polski: ``pl_PL`` (kodowanie ISO-8859-2).

Oba to formy hasłowe (lematy), dzięki czemu porównanie międzyjęzykowe opiera się
na danych tego samego typu i z tego samego źródła. Przygotowane listy (jedno
słowo na linię, UTF-8) trafiają do katalogu docelowego i można je wskazać przez
``--input`` w skryptach eksperymentów. Plików danych nie trzymamy w repozytorium
— generujemy je tym skryptem (``make data``).
"""

import argparse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/LibreOffice/dictionaries/master"


@dataclass(frozen=True)
class HunspellSource:
    """Źródło słownika hunspell dla jednego języka.

    Attributes:
        dic_url: Adres pliku ``.dic``.
        encoding: Kodowanie pliku ``.dic`` (hunspell deklaruje je w ``.aff``;
            pl_PL nie zawiera linii ``SET``, więc podajemy je jawnie).
    """

    dic_url: str
    encoding: str


# Rejestr obsługiwanych języków: etykieta -> źródło hunspell.
SOURCES: dict[str, HunspellSource] = {
    "en": HunspellSource(f"{BASE_URL}/en/en_US.dic", "utf-8"),
    "pl": HunspellSource(f"{BASE_URL}/pl_PL/pl_PL.dic", "iso-8859-2"),
}


def prepare_hunspell(dic_path: Path, out_path: Path, encoding: str = "utf-8", skip_digits: bool = True) -> int:
    """Przekształca słownik hunspell ``.dic`` na prostą listę słów.

    Usuwa nagłówek z liczbą haseł (pierwsza linia), flagi afiksów po znaku ``/``
    oraz — opcjonalnie — hasła zawierające cyfry (np. ``1st``). Duplikaty są
    pomijane. Plik wynikowy zapisywany jest zawsze w UTF-8.

    Args:
        dic_path: Ścieżka do pliku ``.dic``.
        out_path: Ścieżka wynikowej listy słów.
        encoding: Kodowanie pliku źródłowego.
        skip_digits: Czy pomijać hasła zawierające cyfry.

    Returns:
        Liczba zapisanych słów.
    """
    lines = dic_path.read_text(encoding=encoding).splitlines()
    if lines and lines[0].strip().isdigit():
        lines = lines[1:]

    seen: set[str] = set()
    words: list[str] = []
    for line in lines:
        word = line.split("/", 1)[0].strip()
        if not word or word in seen:
            continue
        if skip_digits and any(ch.isdigit() for ch in word):
            continue
        seen.add(word)
        words.append(word)

    out_path.write_text("\n".join(words) + "\n", encoding="utf-8")
    return len(words)


def fetch_language(language: str, out_dir: Path) -> Path:
    """Pobiera słownik danego języka i przygotowuje listę słów.

    Args:
        language: Etykieta języka (klucz z :data:`SOURCES`), używana w nazwach plików.
        out_dir: Katalog na pliki wynikowe.

    Returns:
        Ścieżka przygotowanej listy słów (``<language>.txt``).
    """
    source = SOURCES[language]
    dic_path = out_dir / Path(source.dic_url).name
    if not dic_path.exists():
        print(f"Pobieram słownik [{language}] z {source.dic_url} ...")
        urllib.request.urlretrieve(source.dic_url, dic_path)

    out_path = out_dir / f"{language}.txt"
    count = prepare_hunspell(dic_path, out_path, encoding=source.encoding)
    print(f"[{language}] {count} słów -> {out_path}")
    return out_path


def main() -> None:
    """Punkt wejścia CLI: pobiera i przygotowuje listy słów."""
    parser = argparse.ArgumentParser(description="Pobieranie i przygotowanie list słów do eksperymentów.")
    parser.add_argument("--out-dir", type=Path, default=Path("data/raw"), help="Katalog wyjściowy (domyślnie data/raw)")
    parser.add_argument(
        "--languages",
        nargs="+",
        choices=sorted(SOURCES),
        default=sorted(SOURCES),
        help="Języki do przygotowania (domyślnie: wszystkie)",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for language in args.languages:
        fetch_language(language, args.out_dir)


if __name__ == "__main__":
    main()
