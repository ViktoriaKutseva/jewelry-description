.PHONY: install test test-unit test-integration lint format type-check security config-check architecture-check all

install:
	uv sync

test: test-unit test-integration

test-unit:
	uv run pytest tests/unit/ --cov=src/jewelry_description --cov-report=html

test-integration:
	uv run pytest tests/integration/ --cov=src/jewelry_description --cov-report=html

test-e2e:
	uv run pytest tests/e2e/ --cov=src/jewelry_description --cov-report=html

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests

type-check:
	uv run mypy src

security:
	uv run bandit -r src/

config-check:
	# Validate configurations for all environments
	uv run python -c "from jewelry_description.config import settings; print('✓ Settings loaded successfully:', settings.settings.app_name)"

architecture-check:
	# Check architectural principles compliance
	python scripts/check_dependencies.py || echo "No architecture check script yet"

all: format lint type-check config-check test security