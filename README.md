# Jewelry Cost Calculator

A web-based jewelry cost calculator built with Clean Architecture principles using FastAPI and SQLite.

## 🚀 Quick Start

### Method 1: Using uv (Recommended)
```bash
# Run the web application
uv run jewelry-web

# Or run as module
uv run -m jewelry_description.entrypoints.web.main
```

### Method 2: Using the startup script
```bash
python scripts/run_web.py
# or with uv
uv run python scripts/run_web.py
```

### Method 3: Running as module directly
```bash
python -m jewelry_description.entrypoints.web.main
```

The application will be available at: http://localhost:8000

## 📁 Project Structure

```
├── src/jewelry_description/       # Main application package
│   ├── models/                   # Domain entities
│   ├── business/                 # Business logic and services
│   ├── integrations/             # External dependencies (database)
│   ├── entrypoints/              # Application entry points (web)
│   └── config/                   # Configuration management
├── tests/                        # Test suite
├── scripts/                      # Startup scripts and utilities
├── data/                         # Persistent data storage
├── examples/                     # Example jewelry descriptions
└── pyproject.toml               # Project configuration
```

## 🏗️ Architecture

This project follows Clean Architecture principles:

- **Models**: Domain entities and exceptions
- **Business**: Core business logic, interfaces, and services
- **Integrations**: Database repositories and external services
- **Entrypoints**: Web API endpoints and CLI interfaces
- **Config**: Application configuration and logging setup

## 🌐 Web Interface Features

- **Material Management**: Add and view jewelry materials
- **Cost Calculation**: Calculate total production costs
- **Price Recommendations**: Get suggested retail prices
- **Description Generation**: AI-powered jewelry descriptions
- **Copy-paste Results**: Easy result sharing

## 🔧 Development

### Requirements
- Python 3.12+
- `uv` for dependency management (recommended)

### Setup with uv
```bash
# Install dependencies
uv sync

# Run the application
uv run jewelry-web

# Run tests
uv run pytest

# Run linting
uv run ruff check
uv run mypy src
```

### Alternative Setup (without uv)
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Run application
python run_web.py
```

## 📊 Database

The application uses SQLite with 37+ predefined jewelry materials including:
- Precious metals (silver, copper, brass)
- Gemstones and semi-precious stones
- Findings and components

## 🤖 AI Features

- Automatic jewelry description generation
- Multi-language support (Russian/English)
- Style and material-aware descriptions
- Instagram-ready formatting

## 📝 License

See LICENSE file for details.