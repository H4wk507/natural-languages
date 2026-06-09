# Dane

Plików z danymi (list słów, korpusów) **nie trzymamy w repozytorium** — generujemy
je lokalnie skryptem pobierającym. Katalog `data/raw/` jest ignorowany przez gita.

## Pobranie i przygotowanie

```bash
make data
# lub:
uv run python -m natural_languages.data.fetch
```

Powstają pliki (jedno słowo na linię):

- `data/raw/en.txt` — angielski,
- `data/raw/pl.txt` — polski.

## Źródła

| Język     | Źródło                                                                                            | Licencja     |
| --------- | ------------------------------------------------------------------------------------------------- | ------------ |
| angielski | hunspell LibreOffice [`en_US.dic`](https://github.com/LibreOffice/dictionaries/tree/master/en)    | GPL/LGPL/MPL |
| polski    | hunspell LibreOffice [`pl_PL.dic`](https://github.com/LibreOffice/dictionaries/tree/master/pl_PL) | GPL/LGPL/MPL |

Oba słowniki pobierane są przez HTTPS (cross-platform — bez zależności od słowników
systemowych). To formy hasłowe (lematy); flagi afiksów po znaku `/`, nagłówek z liczbą
haseł oraz hasła zawierające cyfry (np. `1st`) są usuwane przy przygotowaniu listy.
Kodowanie źródeł: angielski UTF-8, polski ISO-8859-2 (wynik zawsze w UTF-8).

## Uruchomienie eksperymentu

```bash
uv run python -m natural_languages.examples.dictionary_stats --input data/raw/pl.txt --language pl
uv run python -m natural_languages.examples.dictionary_stats --input data/raw/en.txt --language en
```

Wyniki (CSV) trafiają do katalogu `results/` (również ignorowanego przez gita).
