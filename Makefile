.PHONY: help install install-dev test test-verbose test-coverage lint format type-check check clean clean-all build pre-commit-install pre-commit-run docs

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
RUFF := ruff
MYPY := mypy
PRE_COMMIT := pre-commit

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*##"; } /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: ## Install package in production mode
	$(PIP) install .

install-dev: ## Install package with development dependencies
	$(PIP) install -e ".[dev]"

##@ Testing

test: ## Run tests
	$(PYTEST) tests/

test-verbose: ## Run tests with verbose output
	$(PYTEST) tests/ -v

test-coverage: ## Run tests with coverage report
	$(PYTEST) tests/ --cov=pwr2 --cov-report=term-missing --cov-report=html --cov-report=xml

test-quick: ## Run tests without coverage
	$(PYTEST) tests/ --no-cov

##@ Code Quality

lint: ## Run linter (ruff)
	$(RUFF) check .

lint-fix: ## Run linter and auto-fix issues
	$(RUFF) check --fix .

format: ## Format code with ruff
	$(RUFF) format .

format-check: ## Check code formatting without changes
	$(RUFF) format --check .

type-check: ## Run type checker (mypy)
	$(MYPY) pwr2

check: lint format-check type-check ## Run all code quality checks

##@ Pre-commit

pre-commit-install: ## Install pre-commit hooks
	$(PRE_COMMIT) install

pre-commit-run: ## Run pre-commit hooks on all files
	$(PRE_COMMIT) run --all-files

pre-commit-update: ## Update pre-commit hooks to latest versions
	$(PRE_COMMIT) autoupdate

##@ Build & Distribution

build: clean ## Build distribution packages
	$(PYTHON) -m build

build-check: build ## Build and check package with twine
	$(PYTHON) -m twine check dist/*

publish-test: build ## Publish to Test PyPI
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI (production)
	$(PYTHON) -m twine upload dist/*

##@ Cleaning

clean: ## Remove build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*.egg' -delete

clean-all: clean ## Remove all generated files including mypy cache
	rm -rf .mypy_cache/
	rm -rf .tox/
	rm -rf venv/
	rm -rf env/

##@ Development Workflow

dev-setup: install-dev pre-commit-install ## Complete development environment setup
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify installation"

dev-check: lint format-check type-check test ## Run all development checks (CI simulation)
	@echo "All checks passed!"

watch-test: ## Run tests in watch mode (requires pytest-watch)
	$(PYTHON) -m pytest_watch

##@ Documentation

docs-serve: ## Serve documentation locally (if using mkdocs)
	@echo "Documentation not yet configured. Consider adding Sphinx or MkDocs."

##@ Utilities

version: ## Show package version
	@$(PYTHON) -c "from pwr2 import __version__; print(__version__)"

deps-update: ## Update dependencies to latest compatible versions
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) list --outdated

deps-tree: ## Show dependency tree
	$(PIP) install pipdeptree 2>/dev/null || true
	pipdeptree

info: ## Show project information
	@echo "Project: pyPWR2"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Location: $$(pwd)"
	@echo "Package version: $$($(PYTHON) -c 'from pwr2 import __version__; print(__version__)' 2>/dev/null || echo 'Not installed')"

##@ Quick Commands

ci: dev-check ## Alias for dev-check (simulate CI locally)

all: clean install-dev check test ## Full clean install and test cycle
	@echo "Complete build and test cycle finished!"
