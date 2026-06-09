# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Package Management
- **Install dependencies**: `uv sync` (installs from lockfile)
- **Run with dependencies**: `uv run <command>` (e.g., `uv run python script.py`)

### Code Quality
- **Lint code**: `make lint` (runs `ruff check .` and `mypy --strict .`)
- **Format code**: `make format` or `uv run ruff format .`
- **Run tests**: `make test` or `uv run pytest`
- **Clean cache**: `make clean` (removes __pycache__, .mypy_cache, .ruff_cache)

### Data
- **Fetch dictionaries**: `make data` or `uv run python -m natural_languages.data.fetch` (downloads hunspell LibreOffice PL/EN word lists into `data/raw/`)

### Documentation
- **Build LaTeX docs**: `make tex` (compiles docs/dokumentacja.tex to PDF)

## Project

Academic project: detecting combinatorial structures (squares, palindromes, abelian squares, shuffled squares, anagrams) in natural language data (dictionaries, corpora). Python, research + experiments + LaTeX/docx documentation.

## Structure

```
.
├── natural_languages/
|   ├── common/           # Shared types (StructureMatch)
|   ├── detectors/        # Structure detectors: squares.py, palindromes.py, abelian.py, anagrams.py, shuffled.py
|   ├── data/             # loader.py, preprocessor.py, fetch.py (download/prepare word lists)
|   ├── examples/         # Example scripts (single_words.py, dictionary_stats.py)
├── tests/                # Pytest tests (test_detectors.py)
├── data/                 # Datasets: README + data/raw/ (downloaded, gitignored)
├── results/              # Experiment CSV output (generated, gitignored)
├── docs/
|   ├── dokumentacja.tex  # LaTeX documentation source (planned)
|   ├── scripts/          # Scripts for generating figures
|   ├── figures/          # Out dir for generated figures
├── Makefile              # Makefile for lint, formating rules etc.
└── pyproject.toml        # Project configuration and dependencies
```

## Stack

- Python 3.12+
- matplotlib / seaborn for charts
- collections.Counter for letter histograms (abelian squares, anagrams)
- No web frameworks — this is a research project, not an application

## Code Style

- Type hints everywhere (`def find_squares(word: str) -> list[tuple[int, int]]`)
- Google-style docstrings
- Variable names in English, comments and docstrings in Polish, project documentation in Polish
- Each detector is a separate module; convention: `check(word)` (whole-word test → bool), `find(word)` (all substructure matches), `find_all(words)` (batch)
- Code must pass `mypy --strict` (enforced by `make lint`)
- Save experiment results as CSV (easy import into documentation tables)

## Domain Context

Combinatorics on words — key concepts:
- **Square**: word of the form `ww` (e.g. kankan = kan+kan)
- **Cube**: word of the form `www` and higher etc.
- **Abelian square**: `w1 w2` where `w2` is an anagram of `w1`
- **Shuffled square**: word decomposable into two identical subsequences
- **Palindrome**: word = its reverse (e.g. kayak)
- Alphabet: letters of a given language. Design decision: `ą ≠ a` (diacritics are separate symbols)
- Normalization: lowercase, no spaces (when analyzing phrases)

## Important

- Detectors must be mathematically correct — verify against definitions from Lothaire.
- Shuffled squares are NP-hard — do not brute-force on long words. Limit to words ≤ 20 characters or use heuristics from TBN posters.
- When comparing across languages, normalize data identically (same pipeline).
- Do not hardcode data paths — use argparse or a config file.
- Dictionaries are fetched via `natural_languages/data/fetch.py` (hunspell LibreOffice; PL=ISO-8859-2, EN=UTF-8, output always UTF-8). `data/raw/` and `results/` are gitignored — regenerate with `make data`.
- Charts: always include axis labels, title, legend. Save as PNG at 300 dpi.
- Tests: every detector must have tests on known examples (kankan → square, kayak → palindrome).

## References

- Lothaire, *Algebraic Combinatorics on Words*, 2002
- Crochemore, Rytter, *Jewels of Stringology*, 2002
- Kolektyw TBN, *Przetasowane kwadraty* 1 & 2 (2024, 2025)
- OEIS (https://oeis.org) — sequences related to square-free words, abelian complexity
