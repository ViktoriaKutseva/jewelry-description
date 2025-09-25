"""
Main FastAPI application for the jewelry cost calculator web interface.
Following Clean Architecture principles with proper dependency injection.
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import os
from loguru import logger

from jewelry_description.config.settings import settings
from jewelry_description.config.logging_config import logging_config
from jewelry_description.business.interfaces import MaterialRepository, DescriptionGenerator
from jewelry_description.business.services import WebJewelryCostService
from .dependencies import (
    create_material_repository,
    create_description_generator,
    create_web_cost_service
)


# Initialize logging
logging_config(settings.log_file)

# Setup FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    debug=settings.debug
)

# Setup templates
template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)


# Pydantic models for request/response
class MaterialRequest(BaseModel):
    """Request model for adding materials."""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Price must be positive")
    unit: str = Field(default="г", max_length=10)
    category: str = Field(default="material", max_length=20)


class MaterialItem(BaseModel):
    """Material item for calculations."""
    name: str
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0) 
    unit: str


class CalculateRequest(BaseModel):
    """Request model for cost calculations."""
    materials: List[MaterialItem] = Field(..., min_length=1)
    hours: float = Field(..., gt=0, le=1000, description="Work hours")
    hourly_rate: float = Field(..., gt=0, le=100000, description="Hourly rate in KZT")
    jewelry_type: str = Field(default="украшение", max_length=50)


class PriceRecommendations(BaseModel):
    """Price recommendations response model."""
    minimal: float
    comfortable: float  
    premium: float


class CalculateResponse(BaseModel):
    """Response model for calculations."""
    total_cost: float
    recommended_prices: PriceRecommendations
    price_comment: str
    description: str


# API Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Serve the main HTML page."""
    logger.info("Serving main page")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/materials")
async def get_all_materials(
    repo: MaterialRepository = Depends(create_material_repository)
) -> Dict[str, List[Dict[str, Any]]]:
    """Get all available materials."""
    logger.info("Fetching all materials via API")
    
    try:
        materials = await repo.get_all()
        logger.info("Successfully returned materials", count=len(materials))
        return {"materials": materials}
        
    except Exception as e:
        logger.error("Failed to fetch materials", error=str(e))
        raise HTTPException(
            status_code=500, 
            detail="Failed to fetch materials from database"
        ) from e


@app.post("/api/materials")
async def add_new_material(
    material: MaterialRequest,
    repo: MaterialRepository = Depends(create_material_repository)
) -> Dict[str, str]:
    """Add a new custom material."""
    logger.info("Adding new material via API", material_name=material.name)
    
    try:
        success = await repo.add(
            name=material.name,
            price=material.price,
            unit=material.unit,
            category=material.category
        )
        
        if success:
            logger.info("Successfully added material", material_name=material.name)
            return {
                "status": "success", 
                "message": f"Material '{material.name}' added successfully"
            }
        else:
            logger.warning("Failed to add material", material_name=material.name)
            raise HTTPException(status_code=400, detail="Failed to add material to database")
            
    except ValueError as e:
        logger.error("Invalid material data", material_name=material.name, error=str(e))
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error("Unexpected error adding material", material_name=material.name, error=str(e))
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while adding material"
        ) from e


@app.post("/api/calculate", response_model=CalculateResponse)
async def calculate_cost(
    request: CalculateRequest,
    cost_service: WebJewelryCostService = Depends(create_web_cost_service),
    description_generator: DescriptionGenerator = Depends(create_description_generator)
) -> CalculateResponse:
    """Calculate jewelry cost and generate description."""
    logger.info(
        "Calculating cost via API",
        jewelry_type=request.jewelry_type,
        materials_count=len(request.materials),
        hours=request.hours,
        hourly_rate=request.hourly_rate
    )
    
    try:
        # Convert Pydantic models to dicts for business layer
        materials_data = [
            {
                "name": mat.name,
                "quantity": mat.quantity,
                "price": mat.price,
                "unit": mat.unit
            }
            for mat in request.materials
        ]
        
        # Calculate cost using business service
        cost_result = cost_service.calculate_with_recommendations(
            materials=materials_data,
            hours=request.hours,
            hourly_rate=request.hourly_rate
        )
        
        # Generate description using business service
        description = description_generator.generate(
            jewelry_type=request.jewelry_type,
            materials=materials_data
        )
        
        response = CalculateResponse(
            total_cost=cost_result["total_cost"],
            recommended_prices=PriceRecommendations(**cost_result["recommended_prices"]),
            price_comment=cost_result["price_comment"],
            description=description
        )
        
        logger.info("Successfully calculated cost and generated description")
        return response
    
    except ValueError as e:
        logger.error("Invalid calculation request", error=str(e))
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error("Failed to calculate cost", error=str(e))
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during calculation"
        ) from e


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "jewelry-calculator"}


@app.get("/test")
async def test_endpoints(
    repo: MaterialRepository = Depends(create_material_repository),
    cost_service: WebJewelryCostService = Depends(create_web_cost_service),
    description_generator: DescriptionGenerator = Depends(create_description_generator)
) -> Dict[str, Any]:
    """Test endpoint to verify all functionality is working."""
    logger.info("Running system test")
    
    try:
        # Test database connection
        materials = await repo.get_all()
        
        # Test calculator with sample data
        sample_materials = [
            {"name": "Test Material", "quantity": 1.0, "price": 100.0, "unit": "г"}
        ]
        
        cost_result = cost_service.calculate_with_recommendations(
            materials=sample_materials,
            hours=2.0,
            hourly_rate=2000.0
        )
        
        description = description_generator.generate(
            jewelry_type="кольцо",
            materials=sample_materials
        )
        
        logger.info("System test completed successfully")
        return {
            "status": "all_systems_working",
            "database_materials_count": len(materials),
            "sample_calculation": cost_result,
            "sample_description_length": len(description)
        }
    
    except Exception as e:
        logger.error("System test failed", error=str(e))
        return {"status": "error", "message": str(e)}


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> HTMLResponse:
    """Handle 404 errors by serving the main page."""
    logger.warning("404 error, redirecting to main page", path=request.url.path)
    return templates.TemplateResponse("index.html", {"request": request}, status_code=404)


def main() -> None:
    """Main entry point for the web application."""
    import uvicorn
    logger.info("Starting jewelry calculator web server")
    uvicorn.run(app, host=settings.web.host, port=settings.web.port)


if __name__ == "__main__":
    main()