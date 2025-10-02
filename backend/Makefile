PYTHON ?= python
PIP := $(PYTHON) -m pip

.PHONY: install install-dev lint test run

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

lint:
	$(PYTHON) -m ruff check app tests

test:
	$(PYTHON) -m pytest

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
