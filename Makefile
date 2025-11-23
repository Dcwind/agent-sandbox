PY ?= python
UV ?= uv

install:
	$(UV) pip install -e .[dev]

run:
	$(UV) run run-agent

lint:
	$(UV) run ruff check

format:
	$(UV) run ruff format

test:
	$(UV) run pytest
