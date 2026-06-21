# TODO

> Część pomysłów inspirowana artykułem prowadzącego (dr B. Pawlik, _The Secret Life of Words_, Chalkdust) — celowo wychodzą poza „podręcznikowe” minimum.

## ⭐ Pomysły wyróżniające (poza minimum)

### Nowe struktury i detektory

- [x] `TangramDetector` — **tangram**: słowo, w którym każda litera występuje parzystą liczbę razy (pojęcie z artykułu prowadzącego). Parzystość to **warunek konieczny** bycia przetasowanym kwadratem → użyć jako szybki pre-filtr przed kosztowną detekcją shuffled square. Do dokumentacji jako lemat: _shuffled square ⟹ tangram_ (plus kontrprzykład, że nie odwrotnie).
- [x] `SquareFreeDetector` — wykrywanie słów **bezkwadratowych** (Thue, 1906) z nawiązaniem do słowa **Prouhet–Thue–Morse**: nad alfabetem 3-literowym istnieją dowolnie długie słowa bezkwadratowe, nad 2-literowym tylko do długości 3.
- [x] Rozszerzyć hierarchię ograniczeń: słowa **overlap-free** oraz **bezkwadratowe abelowo** (abelian-square-free) — ładne do tabeli porównawczej między językami.

### Polowanie na rekordy w językach naturalnych

- [x] Katalog **dwuwyrazowych przetasowanych kwadratów** — odtworzyć wynik Lucasa Mola (9659 par w angielskim) i policzyć analogicznie dla polskiego; porównać liczby między językami. → `analysis/generative.py` (kubełki parzystości) + `examples/two_word_shuffle.py`; pl 19 510, en 5 895, de 4 297, fr 21 065.
- [x] Najdłuższy **jednowyrazowy** shuffled square w każdym języku (ang. _prepress_, _sestet_; fr. _tuteurer_) — poszukać polskich odpowiedników. → `examples/records.py` (zakres „słownik”): pl `ościowościow` (12), en `caucasus` (8), de `generatorgenerator` (18), fr `gagnantgagnant` (14).
- [x] Najdłuższe **zdanie** będące przetasowanym kwadratem — nawiązanie do rekordu 48 liter Saviniena Kreczmana („In nine innings, Eagles battle Boston to soar near Wien win”). → `analysis/phrases.py` + `examples/grammatical_shuffle.py`; rekord gramatyczny 34 znaki („zgody lub niezgody humoru lub niehumoru”), naturalny sufit ~34 z warunku tangramu.

### Eksperymenty „matematyczne” (Do skipa)

- [ ] Mini-eksperyment wokół **otwartego problemu** z artykułu: minimalny rozmiar alfabetu unikającego przetasowanych kwadratów (hipoteza: 4 litery, dowiedzione: 6) — generować słowa nad alfabetem k-literowym i sprawdzać unikanie.
- [ ] Sformułować i udowodnić proste lematy: długość tangramu jest parzysta; shuffled square ⟹ tangram; (ambitne, pytanie otwarte z artykułu) czy istnieją zdania będące przetasowanym kwadratem _przetasowania samych siebie_.

### Algorytmika (z nutą NP-trudności)

- [ ] Rozpoznawanie shuffled square jest **NP-zupełne** (Buss & Sołtys, _Unshuffling a square is NP-hard_) — opisać i zaimplementować ścieżkę: filtr tangramowy → DP/heurystyka dla krótkich słów → ewentualna redukcja do **SAT** dla dłuższych przypadków.
- [ ] Wizualizacje wyróżniające: dot-plot / macierz samonałożeń pokazująca strukturę kwadratu w słowie, wizualizacja słowa Thue-Morse'a, „mapa” liter najczęściej budujących palindromy.

## Detektory

- [ ] `SquareDetector` — dodać detekcję potęg wyższych niż sześciany (n-te potęgi)
- [ ] `ShuffledSquareDetector` — rozważyć heurystyki z plakatów TBN dla słów > 20 znaków
- [ ] `AnagramDetector` — rozważyć obsługę fraz (nie tylko pojedynczych słów)

## Dane

- [ ] **Decyzja o źródłach (do udokumentowania!)**: na razie świadomie zostajemy przy hunspell = **lematy** (formy hasłowe), spójne PL↔EN. Alternatywy z **formami odmienionymi** (fleksja → znacznie więcej kwadratów abelowych) — sparkowane:
  - PL: [Morfologik/PoliMorf](https://github.com/morfologik/polimorfologik) (BSD, ~3,5 M form, 1 zip + TSV) lub [sjp.pl „odmiany”](https://sjp.pl/sl/odmiany/) (CC BY 4.0, 2,76 M); naukowo [SGJP](https://sgjp.pl/) (BSD)
  - EN: [SCOWL](https://wordlist.aspell.net/) (MIT-like, regulowany rozmiar; ~1 h pracy) lub [dwyl words_alpha](https://github.com/dwyl/english-words) (Unlicense, 370 k, 1 plik)
  - sweet spot gdyby wracać: **Morfologik + dwyl** (oba 1-plikowe, czyste licencje, ~1 h łącznie)
- [x] Dodać kolejne języki — **bez przesady**, alfabet już wspiera `TextPreprocessor` (zero zmian w kodzie, słowniki hunspell LibreOffice): _(fr + de zrobione i przeanalizowane)_
  - [x] **francuski** (`fr`) — nawiązuje do _tuteurer_ z artykułu; Romance, uboga fleksja
  - [x] **niemiecki** (`de`) — `äöüß`, złożenia → bardzo długie słowa

## Eksperymenty i przykłady

- [x] Napisać skrypt `examples/phrases.py` — analiza fraz (wielowyrazowych) → zrealizowane jako `examples/grammatical_shuffle.py` (przetasowane kwadraty w kolejnych słowach) i `examples/chiasmus.py` (kwadraty abelowe + palindromy w kolejnych słowach), na bazie `analysis/phrases.py`.
- [x] Napisać skrypt `examples/comparison.py` — porównanie wyników między językami _(porównanie pl/en/de/fr istnieje w `docs/records.ipynb`; dedykowanego skryptu CLI brak)_

## Wykresy

- [x] Rozkład długości znalezionych struktur → histogram długości sklejeń w `docs/records.ipynb` (`two_word_length_hist_pl.png`).
- [x] Porównanie częstości struktur między językami → wykresy słupkowe pl/en/de/fr w `docs/records.ipynb` (`two_word_counts.png`, `two_word_record_length.png`).
- [x] Pamiętać: etykiety osi, tytuł, legenda, PNG 300 dpi → helper `save_fig` zapisuje PNG 300 dpi do `docs/figures/`; każdy wykres ma tytuł i opisy osi.

## Dokumentacja

> Sekcja dla agenta robiącego dokumentację/prezentację. Cały kod jest gotowy i przetestowany
> (58 testów, `ruff` + `mypy --strict` czyste); zadaniem dokumentacji jest **opisać i pokazać**, nie
> dopisywać kodu. Najpierw przeczytaj `CLAUDE.md` i odpal notatniki z `docs/` — tam są wszystkie liczby.
> **Terminologia:** opisuj zjawiska pojęciami z projektu (kwadrat abelowy, palindrom/kwadrat w kolejnych
> słowach); **nie** wprowadzaj terminów retorycznych typu „chiazm”/„antymetabola”.

### Zakres i odbiorca

- [ ] Napisać `docs/dokumentacja.tex` — główny dokument LaTeX (kompilacja: `make tex`)
- [ ] Ustalić odbiorcę: dr B. Pawlik (pasjonat matematyki, autor _The Secret Life of Words_) — premiować **twierdzenia/dowody i kreatywne nawiązania** do jego tematów, nie tylko tabele

### Materiały wejściowe (wszystko już istnieje — nie regenerować bez potrzeby)

- [ ] **Notatniki** (`docs/*.ipynb`) jako źródło wykresów i liczb: `detectors.ipynb` (demo detektorów), `dictionaries.ipynb` (struktury w słowach + ranking języków), `books.ipynb` (types vs tokens w korpusie), `records.ipynb` (rekordy przez granice słów, dwuwyrazowe, sekwencje)
- [ ] **Wykresy** (`docs/figures/*.png`, 300 dpi): `corpus_cross_boundary_records`, `two_word_counts`, `two_word_record_length`, `two_word_length_hist_pl`, `phrase_structure_counts` — wstawiać bezpośrednio do LaTeX
- [ ] **Tabele z CSV** (`results/`): `records_{pl,en,de,fr}.csv` (rekordy), `two_word_shuffle_{pl,en,de,fr}.csv` (sklejenia), `grammatical_shuffle.csv` + `chiasmus.csv` (frazy z korpusu), `{pl,en}_summary.csv`/`_hits.csv` (statystyki słownikowe) → importować jako tabele
- [ ] **Komendy reprodukcji** w aneksie: `make data` (słowniki), `uv run python -m natural_languages.examples.{records,two_word_shuffle,grammatical_shuffle,chiasmus,dictionary_stats} ...`

### Treść merytoryczna

- [ ] **Definicje struktur** (z `CLAUDE.md` „Domain Context”): kwadrat `ww`, sześcian `www`/n-ta potęga, palindrom, kwadrat abelowy `w1w2` (|w1|=|w2|, w2 anagram w1), **tangram** (każda litera parzyście), **przetasowany kwadrat** (rozkład na dwa równe podciągi); decyzja projektowa `ą ≠ a`
- [ ] **Algorytmy** (`natural_languages/analysis/` i `detectors/`): palindrom — **Manacher O(n)** (`palindromes.py::_palindrome_radii`, `analysis/records.py::longest_palindrome`); kwadrat abelowy — **inkrementalny wektor różnic O(1)/krok** (`abelian.py`, `longest_abelian_square`); kwadrat — skan po okresie (`longest_square`); przetasowany kwadrat — **DFS z buforem FIFO + memoizacja + prefiltr tangramowy** (`analysis/records.py::is_shuffled_square`); **kubełki parzystości** dla sklejeń (`generative.py`); **branch-and-bound + round-robin (multiprocessing)** dla korpusu (`examples/records.py`)
- [ ] **Lematy z dowodami** (twierdzenia są punktowane!): _długość tangramu jest parzysta_; _shuffled square ⟹ tangram_ (kontrprzykład `abccba` — tangram, ale nie shuffle square); odnotować, że rozpoznawanie shuffled square jest **NP-zupełne** (Buss & Sołtys 2014) i jak to motywuje kaskadę filtr→DFS
- [ ] **Wyniki — rekordy w słowach (4 języki)**: de króluje przez złożenia (`generatorgenerator` 18, palindrom `reliefpfeiler` 13); pl `niedziadzienia` (abelowy 14); en `sensuousnes` (11), `caucasus` (shuffled 8); fr `gagnantgagnant` (14)
- [ ] **Wyniki — dwuwyrazowe przetasowane kwadraty**: pl 19 510 (rekord 38 `dwudziestkadwójka+dwudziestkachdwójkach`), en 5 895 (26), de 4 297 (40), **fr 21 065, rekord 46** `lieutenantegouverneure+lieutenantesgouverneures` — interpretacja morfologiczna (fr/pl fleksja, de złożenia)
- [ ] **Wyniki — przez granice słów w korpusie (Wolne Lektury)**: palindrom 17, kwadrat 66, **kwadrat abelowy 72** („mgła gęsta ptak czarny skrzydła białe boże …”); w sekwencjach kolejnych słów: przetasowany kwadrat **sufit ~34** („zgody lub niezgody humoru lub niehumoru”) — pokazać kontrast „sens vs długość”
- [ ] **Wydajność** jako osobny akapit: korpus 270 tys. zdań — naiwnie ~5 min → branch-and-bound 82 s → równolegle (10 rdzeni) **28 s**; sklejenia całego słownika pl w **2,9 s** dzięki kubełkom

### Metodyka i ograniczenia

- [ ] Udokumentować **dobór źródeł danych**: hunspell LibreOffice = **lematy** (formy hasłowe), spójne między językami; kodowania (pl ISO-8859-2, de ISO-8859-1, en/fr UTF-8 → wynik UTF-8); normalizacja (małe litery, bez interpunkcji), dedup, odrzucanie haseł z cyframi i flag afiksów. Rozmiary po normalizacji: pl ~302 k, de ~164 k, fr ~79 k, en ~48 k
- [ ] Sekcja **„Ograniczenia”**: lematy vs formy odmienione (fleksja → więcej kwadratów abelowych; sparkowane Morfologik/sjp/SCOWL/dwyl z licencjami — patrz sekcja „Dane”); shuffled square NP-zupełny → limity długości; korpus to próbka 25 MB, nie pełne Wolne Lektury; rekordy zdaniowe to często powtórzenia, nie genuine przeplecenia (filtr `is_repetition`)
- [ ] Odnotować **licencje** danych (hunspell GPL/LGPL/MPL, Wolne Lektury PD/CC-BY-SA) i datę/wersję pobrania słowników

### Bibliografia i prezentacja

- [ ] Dodać bibliografię: Lothaire _Algebraic Combinatorics on Words_ (2002); Crochemore & Rytter _Jewels of Stringology_ (2002); **Pawlik — _The Secret Life of Words_, Chalkdust**; Kolektyw TBN _Przetasowane kwadraty_ 1–2 (2024–25); Thue (1906); Keränen (1992, abelian-square-free); Buss & Sołtys (2014, NP-hardness); L. Mol (dwuwyrazowe shuffle squares); OEIS
- [ ] **Slajdy-perełki** (pod gust prowadzącego): wyścig języków (kto ma najdłuższy X + dlaczego morfologicznie); rekord abelowy 72 z prawdziwej poezji; sufit ~34 dla gramatycznego przetasowanego kwadratu jako napięcie teoria↔język; „kubełki parzystości” jako sprytny trik z artykułu Mola/Pawlika
- [ ] Spójność z `README.md` (po polsku) i strukturą repo z `CLAUDE.md` — nie wprowadzać rozbieżnych nazw modułów/komend
