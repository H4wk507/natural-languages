# Natural Languages

Wykrywanie struktur kombinatorycznych (kwadraty, palindromy, kwadraty abelowe, przetasowane kwadraty, anagramy) w danych z języków naturalnych (słowniki, korpusy).

## Struktura projektu

```
.
├── natural_languages/        # Główny pakiet (kod źródłowy)
│   ├── common/               # Współdzielone typy (StructureMatch)
│   ├── detectors/            # Detektory: squares, palindromes, abelian, anagrams, shuffled
│   ├── data/                 # loader, preprocessor, fetch (pobieranie słowników)
│   └── examples/             # Skrypty przykładowe: single_words, dictionary_stats
├── tests/                    # Testy detektorów (pytest)
├── data/                     # Listy słów: README + data/raw/ (pobierane, ignorowane)
├── results/                  # Wyniki eksperymentów w CSV (generowane, ignorowane)
├── docs/                     # Dokumentacja
│   ├── scripts/              # Skrypty generujące wykresy (matplotlib/seaborn)
│   ├── figures/              # Wyjściowe wykresy (PNG 300 dpi)
│   └── dokumentacja.tex      # Źródło LaTeX (planowane — make tex)
├── CLAUDE.md                 # Wskazówki dla Claude Code
├── Makefile                  # Polecenia: lint, format, test, data, tex, clean
├── pyproject.toml            # Konfiguracja projektu i zależności
├── README.md                 # Ten plik
└── TODO.md                   # Lista zadań i pomysłów
```

## Instalacja

1. Zainstaluj `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Instalacja zależności:

```bash
uv sync
```

## Development

Projekt korzysta z Makefile do typowych zadań:

- `make lint` — Lintowanie (ruff + mypy --strict)
- `make format` — Formatowanie (ruff)
- `make test` — Uruchomienie testów (pytest)
- `make data` — Pobranie i przygotowanie list słów
- `make clean` — Usunięcie plików cache

## Dane i eksperymenty

```bash
make data   # pobiera i przygotowuje listy słów (data/raw/pl.txt, data/raw/en.txt)
uv run python -m natural_languages.examples.dictionary_stats --input data/raw/pl.txt --language pl
```

Szczegóły i źródła danych: [`data/README.md`](data/README.md).
