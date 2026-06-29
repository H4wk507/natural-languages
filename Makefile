clean:
	find . \( -type d -name __pycache__ -o -name "*.pyc" -o -type d -name .mypy_cache -o -type d -name .ruff_cache \) -prune -exec rm -rfv {} \;

lint: 
	uv run ruff check .
	uv run mypy --strict .

format:
	uv run ruff format .

test:
	uv run pytest

data:
	uv run python -m natural_languages.data.fetch

tex:
	cd docs && pdflatex dokumentacja.tex

ANALYSIS_ARCHIVE_NAME = Skowronski-Rapacz-Pietrasik-Malecki-jezyki-naturalne-analiza
zip-analysis:
	rm -rf $(ANALYSIS_ARCHIVE_NAME) $(ANALYSIS_ARCHIVE_NAME).zip
	mkdir -p $(ANALYSIS_ARCHIVE_NAME)
	cp docs/prezentacja.pdf docs/dokumentacja.pdf $(ANALYSIS_ARCHIVE_NAME)/
	cp docs/detectors.ipynb docs/dictionaries.ipynb docs/books.ipynb docs/records.ipynb $(ANALYSIS_ARCHIVE_NAME)/
	zip -9 -r $(ANALYSIS_ARCHIVE_NAME).zip $(ANALYSIS_ARCHIVE_NAME)
	rm -rf $(ANALYSIS_ARCHIVE_NAME)
