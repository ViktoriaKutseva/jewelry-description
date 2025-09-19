# Plan: Convert example_usage.py into an Interactive Web Application (FastAPI, Clean Architecture)

## Goal

Transform the CLI script (`example_usage.py`) into a user-friendly web app:
- Users can **add materials and set price per unit** dynamically.
- Enter quantities, work time, hourly rate, and jewelry metadata.
- See cost breakdown, recommended prices, and price comments.
- Generate Instagram description, export/copy as Markdown or image.

## Prerequisites

- **Project root:** `/home/kutvik/Documents/vscode/jewelry-price-calculator`
- **Source file to convert:** `app/old/example_usage.py`
- **Python version:** 3.12+
- **Dependency management:** `uv` (mandatory)
- **Stack:** FastAPI, Pydantic, Loguru, Pydantic-settings, client-side JS (Fetch API), HTML/CSS
- **Testing:** pytest, pytest-cov
- **Code quality:** ruff, mypy
- **No requirements.txt**, all dependencies in `pyproject.toml`

## Project Structure (src-layout, Clean Architecture)

```
jewelry-description/
├── src/
│   └── jewelry-description/
│       ├── config/
│       │   └── settings.py
│       ├── models/
│       │   └── entities.py
│       ├── business/
│       │   └── services.py
│       ├── integrations/
│       │   └── external_apis/
│       │       └── clients.py
│       └── entrypoints/
│           └── api/
│               ├── main.py
│               ├── routes/
│               ├── schemas.py
│               └── dependencies.py
├── app/
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── js/main.js
│       └── css/style.css
├── tests/
│   └── test_api.py
├── pyproject.toml
└── README.md
```

## Step-by-Step Tasks

### 0. Repository Setup

- Initialize with `uv`:
  - `uv init`
  - Add dependencies:  
    `uv add fastapi httpx pydantic loguru pydantic-settings`
    `uv add --group dev pytest pytest-cov ruff mypy`
- Create folders as above.

### 1. Extract Business Logic

- Move calculation logic from `example_usage.py` to `src/business/services.py`.
- Define input/output models in `src/models/entities.py` using Pydantic.
- Adapter function to accept JSON payload and return calculation result.

### 2. Implement FastAPI Backend

- `src/entrypoints/api/main.py`:
  - GET `/` — serves HTML page.
  - GET `/api/materials` — returns materials from CSV/JSON.
  - POST `/api/calculate` — accepts JSON, returns calculation result.
  - POST `/api/export_md` — returns generated Markdown file (optional).
- Use Loguru for logging, Pydantic-settings for config.

### 3. Build Frontend

- `app/templates/index.html`:
  - Responsive form for materials:
    - **Add Material** button to append new rows.
    - Each row: name (input/dropdown), price per unit (input), quantity (input), unit (input/dropdown), remove button.
  - Inputs for hourly rate, hours, jewelry type, size, style, features, photo URL.
  - Buttons: Calculate, Export MD, Copy Instagram description.
- `app/static/js/main.js`:
  - Fetch `/api/materials` on load for dropdowns.
  - Allow user to add custom materials and prices.
  - Assemble JSON payload on Calculate click.
  - POST to `/api/calculate`, render response.
  - Implement copy-to-clipboard and download MD.

### 4. UX and Validation

- Validate numeric inputs, show inline errors.
- Auto-detect metals vs stones as in CLI.
- Format currency, responsive layout.
- Show generated Instagram description with copy/export.

### 5. Export and Persistence (Optional)

- Client-side download of Markdown file.
- Optionally save data server-side.

### 6. Testing and Quality

- Write pytest tests for calculation endpoint.
- Ensure 90%+ coverage with pytest-cov.
- Lint and type-check with ruff and mypy.

### 7. CI/CD and Deployment

- Setup GitHub Actions workflow:
  - Install uv, run tests, lint, type-check.
- Optionally create Dockerfile for FastAPI app.
- Deploy to VPS/Render/Heroku.

## Example API Payload

```json
{
  "materials": [
    {"name": "Gold", "unit_price": 4200, "quantity": 0.5, "unit": "g"},
    {"name": "Silver", "unit_price": 1200, "quantity": 1.0, "unit": "g"}
  ],
  "consumables": [{"name":"Consumables", "approx_cost":350}],
  "work_time": {"hours": 2.5, "hourly_rate": 2500},
  "electricity_cost": 0,
  "tool_depreciation": 0,
  "packaging_cost": 0,
  "defect_percent": 0,
  "jewelry_meta": {"type":"bracelet","size":"18 cm","style":"boho","features":"gift","photo_url":""}
}
```

## Key Rules

- All dependencies via `uv`, all commands run via `uv run ...`
- Strict separation of layers (models, business, integrations, entrypoints)
- Configuration via pydantic-settings
- Logging via loguru
- Code quality: ruff, mypy, pre-commit
- Tests: 90%+ coverage, E2E for critical flows

## Recommended Commands

- Initialize:  
  `uv init`
- Install dependencies:  
  `uv sync`
- Run server:  
  `uv run python src/entrypoints/api/main.py`
- Run tests:  
  `uv run pytest`

---

**Next Actions:**
1. Move calculation logic to business layer, define Pydantic models.
2. Implement FastAPI API endpoints.
3. Build frontend HTML/JS with dynamic material rows and price per unit input.
4. Add tests, linting, type-checking.
5. Setup CI/CD and deployment.

**Documentation and architecture must follow src-layout and Clean Architecture principles.**