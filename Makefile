.PHONY: help install install-dev test lint format clean build

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

install-dev: ## Install development dependencies
	uv sync --extra dev

test: ## Run tests
	uv run pytest tests/ -v

test-coverage: ## Run tests with coverage
	uv run pytest tests/ --cov=src/raycast_scripts --cov-report=html --cov-report=term

lint: ## Run linting
	uv run ruff check src/ tests/
	uv run mypy src/

format: ## Format code
	uv run ruff format src/ tests/
	uv run isort src/ tests/

format-check: ## Check code formatting
	uv run ruff format --check src/ tests/
	uv run isort --check-only src/ tests/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	uv build

install-hooks: ## Install pre-commit hooks
	uv run pre-commit install

run-todos: ## Run get-todos script
	uv run python scripts/get-todos.py --help

run-polish: ## Run polish-clipboard-text script
	uv run python scripts/polish-clipboard-text.py --help

run-speak: ## Run speak-clipboard script
	uv run python scripts/speak-clipboard.py --help

run-jira: ## Run jira-ticket-info script
	uv run python scripts/jira-ticket-info.py --help

dev-setup: install-dev install-hooks ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make lint' to check code quality"
	@echo "Run 'make format' to format code"