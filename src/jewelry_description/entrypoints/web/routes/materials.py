"""
Materials API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from loguru import logger

from ..dependencies import get_material_repository
from ..schemas import (
    MaterialResponse,
    AddMaterialRequest,
)

router = APIRouter(prefix="/api/v1/materials", tags=["materials"])


@router.get("/", response_model=List[MaterialResponse])
async def get_materials(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in material names"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
):
    """
    Get list of available materials.

    Supports filtering by category and searching by name.
    """
    try:
        logger.info("Getting materials", category=category, search=search, limit=limit)

        repo = get_material_repository()

        if category == "filtered" or (category is None and search is None):
            # Return filtered materials for common use
            materials = repo.get_filtered_materials()
        else:
            # Return all materials from CSV
            materials = repo.load_materials_from_csv()

        # Apply filters
        if search:
            search_lower = search.lower()
            materials = [m for m in materials if search_lower in m.name.lower()]

        # Apply limit
        materials = materials[:limit]

        # Convert to response model
        response = [
            MaterialResponse(
                name=m.name,
                unit_price=m.unit_price,
                unit=m.unit,
                category="material"
            )
            for m in materials
        ]

        logger.info("Materials retrieved successfully", count=len(response))
        return response

    except Exception as e:
        logger.error("Failed to get materials", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve materials"
        )


@router.post("/", response_model=MaterialResponse, status_code=201)
async def add_material(request: AddMaterialRequest):
    """
    Add a custom material.

    Note: Currently this is a placeholder - materials are read-only from CSV.
    In a full implementation, this would add materials to a database.
    """
    try:
        logger.info("Adding custom material", material_name=request.name)

        # For now, return the material as if it was added
        # In a real implementation, this would save to database
        response = MaterialResponse(
            name=request.name,
            unit_price=request.unit_price,
            unit=request.unit,
            category=request.category
        )

        logger.info("Material added successfully", material_name=request.name)
        return response

    except Exception as e:
        logger.error("Failed to add material", error=str(e), material_name=request.name)
        raise HTTPException(
            status_code=500,
            detail="Failed to add material"
        )


@router.get("/search", response_model=List[MaterialResponse])
async def search_materials(q: str = Query(..., min_length=1, max_length=100)):
    """
    Search materials by name.
    """
    try:
        logger.info("Searching materials", query=q)

        repo = get_material_repository()
        materials = repo.load_materials_from_csv()

        # Search by name (case-insensitive partial match)
        query_lower = q.lower()
        filtered_materials = [
            m for m in materials
            if query_lower in m.name.lower()
        ]

        response = [
            MaterialResponse(
                name=m.name,
                unit_price=m.unit_price,
                unit=m.unit,
                category="material"
            )
            for m in filtered_materials
        ]

        logger.info("Material search completed", query=q, results=len(response))
        return response

    except Exception as e:
        logger.error("Failed to search materials", error=str(e), query=q)
        raise HTTPException(
            status_code=500,
            detail="Failed to search materials"
        )