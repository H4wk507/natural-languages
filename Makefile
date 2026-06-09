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
