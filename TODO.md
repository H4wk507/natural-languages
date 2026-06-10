# TODO

> Część pomysłów inspirowana artykułem prowadzącego (dr B. Pawlik, _The Secret Life of Words_, Chalkdust) — celowo wychodzą poza „podręcznikowe” minimum.

## ⭐ Pomysły wyróżniające (poza minimum)

### Nowe struktury i detektory

- [x] `TangramDetector` — **tangram**: słowo, w którym każda litera występuje parzystą liczbę razy (pojęcie z artykułu prowadzącego). Parzystość to **warunek konieczny** bycia przetasowanym kwadratem → użyć jako szybki pre-filtr przed kosztowną detekcją shuffled square. Do dokumentacji jako lemat: _shuffled square ⟹ tangram_ (plus kontrprzykład, że nie odwrotnie).
- [x] `SquareFreeDetector` — wykrywanie słów **bezkwadratowych** (Thue, 1906) z nawiązaniem do słowa **Prouhet–Thue–Morse**: nad alfabetem 3-literowym istnieją dowolnie długie słowa bezkwadratowe, nad 2-literowym tylko do długości 3.
- [x] Rozszerzyć hierarchię ograniczeń: słowa **overlap-free** oraz **bezkwadratowe abelowo** (abelian-square-free) — ładne do tabeli porównawczej między językami.

### Polowanie na rekordy w językach naturalnych

- [ ] Najdłuższe **słowo bezkwadratowe** w słowniku każdego języka — ranking + ciekawostki (czy w ogóle istnieją długie słowa bez powtórzonego bloku?).
- [ ] Katalog **dwuwyrazowych przetasowanych kwadratów** — odtworzyć wynik Lucasa Mola (9659 par w angielskim) i policzyć analogicznie dla polskiego; porównać liczby między językami.
- [ ] Najdłuższy **jednowyrazowy** shuffled square w każdym języku (ang. _prepress_, _sestet_; fr. _tuteurer_) — poszukać polskich odpowiedników.
- [ ] Najdłuższe **zdanie** będące przetasowanym kwadratem — nawiązanie do rekordu 48 liter Saviniena Kreczmana („In nine innings, Eagles battle Boston to soar near Wien win”).

### Łamigłówki i smaczki na prezentację

- [ ] Odtworzyć **zagadkę-bonus z artykułu**: które zdanie jest shuffled square? („He heard a ruckus: a duck hushed a red ara” vs „…a duck used a red rattle at the lead head”) — mały interaktywny weryfikator.
- [ ] Polowanie na **„anagramy-równania”** w stylu `elevenplustwo` / `twelveplusone` (oba = 13): przeszukać słownie zapisane liczebniki w kilku językach i znaleźć pary anagramowe o równej wartości liczbowej.
- [ ] Galeria słynnych przykładów do dokumentacji/prezentacji: palindromy zdaniowe („Kobyła ma mały bok”, „A man, a plan, a canal: Panama”), kwadraty (kankan, czacza), kwadrat abelowy (kryptoportyk).

### Eksperymenty „matematyczne” (twierdzenia/dowody są punktowane w kryteriach!)

- [ ] Mini-eksperyment wokół **otwartego problemu** z artykułu: minimalny rozmiar alfabetu unikającego przetasowanych kwadratów (hipoteza: 4 litery, dowiedzione: 6) — generować słowa nad alfabetem k-literowym i sprawdzać unikanie.
- [ ] Zliczać znalezione struktury i dopasować do ciągów **OEIS** (np. liczba słów bezkwadratowych, złożoność abelowa) — niezależna weryfikacja poprawności detektorów.
- [ ] Sformułować i udowodnić proste lematy: długość tangramu jest parzysta; shuffled square ⟹ tangram; (ambitne, pytanie otwarte z artykułu) czy istnieją zdania będące przetasowanym kwadratem _przetasowania samych siebie_.

### Algorytmika (z nutą NP-trudności)

- [ ] Rozpoznawanie shuffled square jest **NP-zupełne** (Buss & Sołtys, _Unshuffling a square is NP-hard_) — opisać i zaimplementować ścieżkę: filtr tangramowy → DP/heurystyka dla krótkich słów → ewentualna redukcja do **SAT** dla dłuższych przypadków.
- [ ] Wizualizacje wyróżniające: dot-plot / macierz samonałożeń pokazująca strukturę kwadratu w słowie, wizualizacja słowa Thue-Morse'a, „mapa” liter najczęściej budujących palindromy.

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
- [ ] Dodać bibliografię (Lothaire, Crochemore & Rytter, TBN, OEIS, **Pawlik — _The Secret Life of Words_, Chalkdust**, Thue 1906, Buss & Sołtys 2014)
