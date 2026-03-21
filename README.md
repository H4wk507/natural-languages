# Natural Languages

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

Project uses Makefile for some development tasks:

- `make lint` - Lint using ruff
- `make format` - Format using ruff
- `make clean` - Remove cache files
