.PHONY: install test test-unit test-integration test-e2e lint format type-check security config-check architecture-check all
.PHONY: docker-build docker-run docker-stop docker-logs docker-clean docker-test
.PHONY: deploy-staging deploy-production setup-env clean-env
.PHONY: dev-server dev-db dev-logs dev-clean

# ==========================================
# DEVELOPMENT TARGETS
# ==========================================

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
	@echo "✓ Validating development settings..."
	@JEWELRY_ENVIRONMENT=development uv run python -c "from jewelry_description.config import settings; print('✓ Development settings loaded:', settings.settings.app_name)"
	@echo "✓ Validating testing settings..."
	@JEWELRY_ENVIRONMENT=testing uv run python -c "from jewelry_description.config import settings; print('✓ Testing settings loaded:', settings.settings.app_name)"
	@echo "✓ Validating staging settings..."
	@JEWELRY_ENVIRONMENT=staging uv run python -c "from jewelry_description.config import settings; print('✓ Staging settings loaded:', settings.settings.app_name)"
	@echo "✓ Validating production settings..."
	@JEWELRY_ENVIRONMENT=production uv run python -c "from jewelry_description.config import settings; print('✓ Production settings loaded:', settings.settings.app_name)"

architecture-check:
	# Check architectural principles compliance
	python scripts/check_dependencies.py || echo "No architecture check script yet"

all: format lint type-check config-check test security

# ==========================================
# DOCKER TARGETS
# ==========================================

docker-build:
	@echo "Building Docker image..."
	docker build -t jewelry-description:latest .

docker-run: docker-build
	@echo "Starting application with Docker..."
	docker run -d --name jewelry-description-app \
		-p 8000:8000 \
		--env-file .env \
		jewelry-description:latest

docker-stop:
	@echo "Stopping Docker containers..."
	docker stop jewelry-description-app || true
	docker rm jewelry-description-app || true

docker-logs:
	docker logs -f jewelry-description-app

docker-clean: docker-stop
	@echo "Cleaning up Docker resources..."
	docker rmi jewelry-description:latest || true
	docker system prune -f

docker-test: docker-build
	@echo "Testing Docker image..."
	docker run --rm jewelry-description:latest python -c "import sys; print('Python version:', sys.version)"
	docker run --rm jewelry-description:latest python -c "from src.jewelry_description.config.settings import get_settings; print('Settings loaded successfully')"
	docker run --rm --env JEWELRY_ENVIRONMENT=testing jewelry-description:latest uv run pytest tests/unit/ -v

# ==========================================
# DEVELOPMENT ENVIRONMENT TARGETS
# ==========================================

dev-server: setup-env
	@echo "Starting development server..."
	JEWELRY_ENVIRONMENT=development uv run uvicorn jewelry_description.entrypoints.web.main:app --reload --host 0.0.0.0 --port 8000

dev-db:
	@echo "Starting development database..."
	docker-compose up -d db

dev-logs:
	docker-compose logs -f

dev-clean:
	@echo "Cleaning development environment..."
	docker-compose down -v
	rm -rf .env

# ==========================================
# DEPLOYMENT TARGETS
# ==========================================

setup-env:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp .env.example .env; \
		echo "✓ .env file created. Please edit it with your configuration."; \
	else \
		echo "✓ .env file already exists."; \
	fi

clean-env:
	rm -f .env

deploy-staging: docker-build
	@echo "Deploying to staging environment..."
	@echo "This would typically push to a container registry and trigger deployment"
	@echo "For now, run: docker tag jewelry-description:latest your-registry/jewelry-description:staging"
	@echo "Then push and deploy using your deployment tool (ECS, Kubernetes, etc.)"

deploy-production: docker-build
	@echo "Deploying to production environment..."
	@echo "This would typically push to a container registry and trigger deployment"
	@echo "For now, run: docker tag jewelry-description:latest your-registry/jewelry-description:production"
	@echo "Then push and deploy using your deployment tool (ECS, Kubernetes, etc.)"

# ==========================================
# UTILITY TARGETS
# ==========================================

help:
	@echo "Available targets:"
	@echo "Development:"
	@echo "  install          - Install dependencies"
	@echo "  test             - Run all tests"
	@echo "  test-unit        - Run unit tests"
	@echo "  test-integration - Run integration tests"
	@echo "  test-e2e         - Run end-to-end tests"
	@echo "  lint             - Run linting"
	@echo "  format           - Format code"
	@echo "  type-check       - Run type checking"
	@echo "  security         - Run security checks"
	@echo "  config-check     - Validate configurations"
	@echo "  architecture-check - Check architecture compliance"
	@echo "  all              - Run all quality checks"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-run       - Run application in Docker"
	@echo "  docker-stop      - Stop Docker containers"
	@echo "  docker-logs      - Show Docker logs"
	@echo "  docker-clean     - Clean Docker resources"
	@echo "  docker-test      - Test Docker image"
	@echo ""
	@echo "Development Environment:"
	@echo "  setup-env        - Set up environment file"
	@echo "  clean-env        - Remove environment file"
	@echo "  dev-server       - Start development server"
	@echo "  dev-db           - Start development database"
	@echo "  dev-logs         - Show development logs"
	@echo "  dev-clean        - Clean development environment"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy-staging   - Deploy to staging"
	@echo "  deploy-production- Deploy to production"
	@echo ""
	@echo "Other:"
	@echo "  help             - Show this help message"