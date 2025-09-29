"""
FastAPI web application for jewelry cost calculation and description generation.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from jewelry_description.config.logging_config import setup_logging
from jewelry_description.config.settings import settings

from .routes.materials import router as materials_router
from .routes.calculator import router as calculator_router
from .routes.descriptions import router as descriptions_router
from .routes.health import router as health_router
from .errors import setup_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    setup_logging()
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Add url_for to template context
def url_for(name: str, **path_params):
    if name == 'static':
        filename = path_params.get('filename', '')
        return f"/static/{filename}"
    return f"/{name}"

templates.env.globals['url_for'] = url_for

# Include routers
app.include_router(materials_router)
app.include_router(calculator_router)
app.include_router(descriptions_router)
app.include_router(health_router)


@app.get("/")
async def root():
    """Root endpoint - redirect to main calculator page."""
    return {"message": "Jewelry Calculator API", "docs": "/docs", "health": "/health"}


@app.get("/calculator")
async def calculator_page(request: Request):
    """Main calculator web page."""
    return templates.TemplateResponse("index.html", {"request": request})
