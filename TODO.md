# TODO

## Detektory

- [ ] `SquareDetector` — dodać detekcję potęg wyższych niż sześciany (n-te potęgi)
- [ ] `ShuffledSquareDetector` — rozważyć heurystyki z plakatów TBN dla słów > 20 znaków
- [ ] `PalindromeDetector` — zoptymalizować algorytm (obecnie O(n³), można O(n²) algorytmem Manachera)
- [ ] `AbelianSquareDetector` — zoptymalizować przez inkrementalne aktualizowanie Countera zamiast tworzenia nowego w każdej iteracji
- [ ] `AnagramDetector` — rozważyć obsługę fraz (nie tylko pojedynczych słów)

## Dane

- [ ] Zebrać i dodać słowniki do analizy (polski, angielski, inne języki)
- [ ] Zebrać korpusy tekstowe do eksperymentów
- [ ] Rozszerzyć `TextPreprocessor` o obsługę większej liczby alfabetów (np. cyrylica, inne języki europejskie)
- [ ] Dodać walidację danych wejściowych w `DataLoader`

## Eksperymenty i przykłady

- [ ] Napisać skrypt `examples/phrases.py` — analiza fraz (wielowyrazowych)
- [ ] Napisać skrypt `examples/comparison.py` — porównanie wyników między językami
- [ ] Eksperymenty na słownikach: statystyki występowania kwadratów, palindromów itp.
- [ ] Zapisywać wyniki eksperymentów jako CSV

## Wykresy

- [ ] Skrypty w `docs/scripts/` do generowania wykresów (matplotlib/seaborn)
- [ ] Rozkład długości znalezionych struktur
- [ ] Porównanie częstości struktur między językami
- [ ] Pamiętać: etykiety osi, tytuł, legenda, PNG 300 dpi

## Dokumentacja

- [ ] Napisać `docs/dokumentacja.tex` — główny dokument LaTeX
- [ ] Opisać definicje matematyczne struktur
- [ ] Opisać algorytmy użyte w detektorach
- [ ] Zamieścić wyniki eksperymentów (tabele z CSV, wykresy)
- [ ] Dodać bibliografię (Lothaire, Crochemore & Rytter, TBN, OEIS)
