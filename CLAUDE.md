# CLAUDE.md

## Project

Academic project: detecting combinatorial structures (squares, palindromes, abelian squares, shuffled squares, anagrams) in natural language data (dictionaries, corpora). Python, research + experiments + LaTeX/docx documentation.

## Structure

```
src/
  detectors/       # Structure detectors: squares.py, palindromes.py, abelian.py, anagrams.py, shuffled.py
  data/            # loader.py, preprocessor.py (tokenization, normalization)
  experiments/     # Experiment scripts (single_words.py, phrases.py, comparison.py)
  utils/           # stats.py, viz.py (matplotlib/seaborn)
data/              # Dictionaries, corpora
results/           # Experiment outputs: CSV + PNG charts
docs/              # Project documentation
tests/             # Unit tests (pytest)
```

## Commands

- `python -m pytest tests/` — run tests
- `python -m src.experiments.single_words --lang pl` — dictionary experiments
- `python -m src.experiments.phrases --corpus data/nkjp_sample.txt` — corpus experiments
- `uv sync` — dependencies

## Stack

- Python 3.11+
- pytest for testing
- matplotlib / seaborn for charts
- collections.Counter for letter histograms (abelian squares, anagrams)
- No web frameworks — this is a research project, not an application

## Code Style

- Type hints everywhere (`def find_squares(word: str) -> list[tuple[int, int]]`)
- Google-style docstrings
- Variable names and comments in English, project documentation in Polish
- Each detector is a separate module with a main function and a `find_all(words)` function for batch processing
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
- Charts: always include axis labels, title, legend. Save as PNG at 300 dpi.
- Tests: every detector must have tests on known examples (kankan → square, kayak → palindrome).

## References

- Lothaire, *Algebraic Combinatorics on Words*, 2002
- Crochemore, Rytter, *Jewels of Stringology*, 2002
- Kolektyw TBN, *Przetasowane kwadraty* 1 & 2 (2024, 2025)
- OEIS (https://oeis.org) — sequences related to square-free words, abelian complexity
