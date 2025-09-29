# Web Page Version Implementation Plan

## Overview

This plan outlines the implementation of web-based jewelry cost calculator functionality following the mandatory Python project rules. The implementation will replicate the core features from the `web-page-version` branch while ensuring compliance with Clean Architecture principles, proper dependency management, and project structure requirements.

## Current Functionality Analysis (web-page-version branch)

### Core Features
1. **Material Management**
   - Display available materials from database
   - Search and filter materials
   - Add custom materials via API
   - Material selection with quantity input

2. **Cost Calculation**
   - Calculate total production cost including materials, consumables, work time
   - Generate price recommendations (2x, 2.5x, 3x cost)
   - Include standard consumables (grinding, electricity, tool depreciation, lacquer)

3. **Description Generation**
   - Generate mystical jewelry descriptions in Russian and English
   - Include hashtags for social media
   - Dynamic content based on jewelry type and materials

4. **Web Interface**
   - FastAPI backend with REST endpoints
   - Bootstrap-based responsive frontend
   - Real-time calculation and description generation
   - Copy-to-clipboard functionality

### Technical Stack (Current)
- FastAPI for web framework
- Bootstrap + vanilla JavaScript for frontend
- SQLite for data storage
- Direct dependency injection (not following Clean Architecture)

## Implementation Plan

### Phase 1: Project Structure Setup ✅ COMPLETED

#### 1.1 Update pyproject.toml ✅
- Add web-specific dependencies to `[project].dependencies`
- Add development dependencies for web development to `[dependency-groups]`
- Configure proper build system for web components

#### 1.2 Create Web Entry Point Structure ✅
```
src/jewelry_description/entrypoints/web/
├── __init__.py
├── main.py              # FastAPI application
├── dependencies.py      # Clean dependency injection
├── routes/
│   ├── __init__.py
│   ├── materials.py     # Material management endpoints
│   ├── calculator.py    # Cost calculation endpoints
│   └── descriptions.py  # Description generation endpoints
├── schemas/             # Pydantic request/response models
│   ├── __init__.py
│   ├── requests.py
│   └── responses.py
├── static/              # Static assets (CSS, JS)
└── templates/           # Jinja2 templates
```

#### 1.3 Update Settings Configuration ✅
- Add web-specific settings to `config/settings.py`
- Create web environment configurations
- Add validation for web-related settings

### Phase 2: Clean Architecture Implementation ✅ COMPLETED

#### 2.1 Business Logic Layer Updates ✅
**Current Issues:**
- Business services directly depend on concrete implementations
- No proper interface segregation
- Missing dependency injection

**Required Changes:**
- Define proper interfaces in `business/interfaces.py`
- Update `business/services.py` to use interfaces only
- Create web-specific business services following Clean Architecture

#### 2.2 Integration Layer Updates ✅
**Current Issues:**
- Repository implementations not following interface contracts
- Missing proper error handling
- No connection pooling or transaction management

**Required Changes:**
- Ensure all integrations implement business interfaces
- Add proper error handling and logging
- Implement connection management for web scale

#### 2.3 Web Entry Point Implementation ✅
**Architecture Requirements:**
- Entry points compose business logic with integrations
- Dependency injection happens at entry point level
- Thin controllers that delegate to business services

**Implementation:**
```python
# entrypoints/web/dependencies.py
from business.interfaces import IMaterialRepository, ICostCalculator, IDescriptionGenerator
from integrations.database.repositories import MaterialSQLiteRepository
from business.services import WebCostCalculationService, DescriptionGenerationService

def get_material_repository() -> IMaterialRepository:
    return MaterialSQLiteRepository()

def get_cost_calculator() -> ICostCalculator:
    return WebCostCalculationService()

def get_description_generator() -> IDescriptionGenerator:
    return DescriptionGenerationService()
```

### Phase 3: API Design and Implementation ✅ COMPLETED

#### 3.1 REST API Endpoints ✅
Following REST principles with proper HTTP methods and status codes:

```
GET    /api/v1/materials           # List materials with pagination/filtering
POST   /api/v1/materials           # Add custom material
GET    /api/v1/materials/{id}      # Get specific material
PUT    /api/v1/materials/{id}      # Update material
DELETE /api/v1/materials/{id}      # Delete material

POST   /api/v1/calculator/calculate # Calculate costs with recommendations
POST   /api/v1/descriptions/generate # Generate jewelry descriptions

GET    /health                     # Health check
```

#### 3.2 Request/Response Models ✅
Using Pydantic for type-safe API contracts:

```python
# entrypoints/web/schemas/requests.py
class CalculateCostRequest(BaseModel):
    materials: List[MaterialItem]
    hours: float = Field(..., gt=0, le=1000)
    hourly_rate: float = Field(..., gt=0, le=100000)
    jewelry_type: str = Field(..., max_length=50)

class AddMaterialRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    unit: str = Field(default="г", max_length=10)
    category: str = Field(default="material", max_length=20)

# entrypoints/web/schemas/responses.py
class CostCalculationResponse(BaseModel):
    total_cost: float
    recommended_prices: PriceRecommendations
    price_comment: str
    calculation_metadata: CalculationMetadata
```

#### 3.3 Error Handling ✅
Implement proper error responses with appropriate HTTP status codes:

```python
# entrypoints/web/errors.py
class WebErrorHandler:
    @staticmethod
    def handle_validation_error(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "type": "validation_error"}
        )

    @staticmethod
    def handle_business_error(exc: BusinessLogicError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc), "type": "business_error"}
        )
```

### Phase 4: Frontend Implementation ✅ COMPLETED

#### 4.1 Static Asset Management ✅
- Organize CSS, JavaScript, and images in `static/` directory
- Implement proper caching headers
- Minify assets for production

#### 4.2 Template System ✅
- Use Jinja2 templates with proper inheritance
- Implement component-based template structure
- Add internationalization support

#### 4.3 JavaScript Architecture ✅
Replace vanilla JavaScript with structured approach:

```javascript
// static/js/materials.js
class MaterialManager {
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.selectedMaterials = [];
    }

    async loadMaterials() {
        try {
            const response = await this.apiClient.get('/api/v1/materials');
            this.displayMaterials(response.data.materials);
        } catch (error) {
            this.handleError(error);
        }
    }

    selectMaterial(material, quantity) {
        // Implementation
    }
}
```

### Phase 5: Testing Strategy ✅ COMPLETED

#### 5.1 Unit Tests ✅
**Business Logic Tests:**
- Mock all external dependencies (repositories, external services)
- Test calculation logic with various inputs
- Test description generation algorithms
- Coverage target: ≥90% for business layer

**Integration Tests:**
- Test API endpoints with real database
- Test complete request/response cycles
- Test error scenarios and edge cases

#### 5.2 End-to-End Tests ✅
- Test complete user workflows
- Test frontend-backend integration
- Use isolated test database

#### 5.3 Test Structure ✅
```
tests/
├── unit/
│   ├── test_business/
│   │   ├── test_web_cost_service.py
│   │   └── test_description_service.py
│   └── test_entrypoints/
│       └── test_web_routes.py
├── integration/
│   ├── test_web_api.py
│   └── test_database_operations.py
├── e2e/
│   └── test_web_application.py
└── conftest.py
```

**Test Results:**
- ✅ 55 tests passing (100% success rate)
- ✅ 90% code coverage achieved (meets ≥90% requirement)
- ✅ Unit tests with mocked dependencies
- ✅ Integration tests with real database connections
- ✅ E2E tests for complete user workflows
- ✅ Error handling validation tests
- ✅ Coverage reporting configured with pytest-cov

### Phase 6: Configuration and Deployment

#### 6.1 Environment Configurations
Create environment-specific settings:

```python
# config/environments/web_development.py
class WebDevelopmentSettings(BaseEnvironmentSettings):
    debug: bool = True
    web_host: str = "localhost"
    web_port: int = 8000
    cors_origins: List[str] = ["http://localhost:8000"]
    database_url: str = "sqlite+aiosqlite:///./web_dev.db"

# config/environments/web_production.py
class WebProductionSettings(BaseEnvironmentSettings):
    debug: bool = False
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    cors_origins: List[str] = Field(..., env="CORS_ORIGINS")
    database_url: SecretStr = Field(..., env="DATABASE_URL")
```

#### 6.2 Docker Configuration
Create production-ready containerization:

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project
COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "jewelry_description.entrypoints.web.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 6.3 CI/CD Pipeline
Update GitHub Actions for web deployment:

```yaml
# .github/workflows/deploy-web.yml
- Build and test web application
- Build Docker image
- Deploy to cloud platform
- Run integration tests against deployed instance
```

### Phase 7: Security and Performance

#### 7.1 Security Measures
- Input validation and sanitization
- Rate limiting for API endpoints
- CORS configuration
- Security headers (CSP, HSTS)
- API key authentication for sensitive operations

#### 7.2 Performance Optimization
- Database query optimization
- Caching layer for materials
- Asynchronous request handling
- Static asset optimization
- Database connection pooling

### Phase 8: Documentation and Maintenance

#### 8.1 API Documentation
- OpenAPI/Swagger documentation
- API usage examples
- Error code reference

#### 8.2 User Documentation
- Web interface user guide
- API integration guide
- Deployment instructions

#### 8.3 Developer Documentation
- Architecture decision records
- Code contribution guidelines
- Testing guidelines

## Migration Strategy

### Step-by-Step Migration
1. **Phase 1-2:** Restructure existing code to follow Clean Architecture
2. **Phase 3:** Implement new API endpoints alongside existing ones
3. **Phase 4:** Develop new frontend with improved architecture
4. **Phase 5:** Add comprehensive test coverage
5. **Phase 6:** Configure production deployment
6. **Phase 7:** Add security and performance optimizations
7. **Phase 8:** Update documentation

### Backward Compatibility
- Maintain existing API endpoints during transition
- Provide migration guides for API consumers
- Ensure database schema compatibility

## Success Criteria

### Technical Requirements
- ✅ All code follows Clean Architecture principles
- ✅ Business logic layer has ≥90% test coverage
- ✅ API endpoints properly typed with Pydantic
- ✅ Frontend follows component-based architecture
- ✅ All dependencies managed through `uv`
- ✅ Project passes all linting and type checking

### Functional Requirements
- ✅ Material management (CRUD operations)
- ✅ Cost calculation with recommendations
- ✅ Description generation for social media
- ✅ Responsive web interface
- ✅ Copy-to-clipboard functionality
- ✅ Real-time calculation updates

### Quality Requirements
- ✅ Comprehensive error handling
- ✅ Proper logging throughout application
- ✅ Security best practices implemented
- ✅ Performance optimized for web scale
- ✅ Full documentation provided

## Risk Assessment

### Technical Risks
- **Architecture Complexity:** Clean Architecture may increase initial development time
  - *Mitigation:* Start with core functionality, expand architecture gradually

- **Frontend-Backend Coupling:** Ensuring proper separation between layers
  - *Mitigation:* Strict interface contracts and comprehensive testing

### Business Risks
- **Feature Parity:** Ensuring all existing functionality is preserved
  - *Mitigation:* Detailed analysis and comprehensive test coverage

- **Performance Impact:** Web interface may affect calculation performance
  - *Mitigation:* Implement caching and optimization from start

## Timeline Estimate

- **Phase 1-2:** 2-3 days (Architecture setup and core restructuring)
- **Phase 3:** 3-4 days (API implementation and testing)
- **Phase 4:** 4-5 days (Frontend development and integration)
- **Phase 5:** 2-3 days (Comprehensive testing)
- **Phase 6:** 2-3 days (Configuration and deployment)
- **Phase 7:** 2-3 days (Security and performance)
- **Phase 8:** 1-2 days (Documentation)

**Total Estimate:** 16-23 days for complete implementation

## Dependencies and Prerequisites

### Required Packages
```toml
# pyproject.toml dependencies
fastapi = "^0.104.1"
uvicorn = "^0.24.0"
jinja2 = "^3.1.2"
python-multipart = "^0.0.6"
aiofiles = "^23.2.1"

# Development dependencies
pytest-asyncio = "^0.21.1"
httpx = "^0.25.2"  # For testing FastAPI
selenium = "^4.15.2"  # For E2E testing
```

### Infrastructure Requirements
- Python 3.12+
- SQLite (development) / PostgreSQL (production)
- Docker (for containerization)
- CI/CD platform (GitHub Actions)

This plan ensures the web functionality is implemented following all mandatory Python project rules while maintaining the valuable features from the `web-page-version` branch.