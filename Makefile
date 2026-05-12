SHELL := /bin/bash

POETRY := poetry
CMD := $(POETRY) run

SRC := src
TESTS := tests

RUN_MODULE := src.main

.DEFAULT_GOAL := help

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nAvailable commands:\n\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install project dependencies with Poetry
	$(POETRY) install

check: ## Validate pyproject.toml and dependency definitions
	$(POETRY) check

format: ## Format source code and tests with black
	$(CMD) black $(SRC) $(TESTS) --target-version py313 .

format-check: ## Check formatting without modifying files
	$(CMD) black --check $(SRC) $(TESTS) --target-version py313 .

lint: ## Run ruff on source code and tests
	$(CMD) ruff check $(SRC) $(TESTS)

lint-fix: ## Automatically fix lint issues that ruff can handle
	$(CMD) ruff check --fix $(SRC) $(TESTS)

type-check: ## Run mypy on the source code
	$(CMD) mypy $(SRC)

test: ## Run test suite with pytest
	$(CMD) pytest $(TESTS) -v

test-cov: ## Run tests with coverage report
	$(CMD) pytest $(TESTS) --cov=$(SRC) --cov-report=term-missing

run: ## Run the data pipeline
	$(CMD) python -m $(RUN_MODULE)

fix: format lint-fix ## Apply automatic formatting and lint fixes

qa: format-check lint type-check test ## Run the full quality checks

clean: ## Remove temporary files and tool caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete

.PHONY: help install check format format-check lint lint-fix type-check test test-cov run fix qa clean
