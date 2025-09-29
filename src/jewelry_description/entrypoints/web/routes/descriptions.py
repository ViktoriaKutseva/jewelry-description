"""
Descriptions API endpoints.
"""

from fastapi import APIRouter, HTTPException
from loguru import logger

from ..dependencies import get_description_generator
from ..schemas import (
    GenerateDescriptionRequest,
    DescriptionGenerationResponse,
)


router = APIRouter(prefix="/api/v1/descriptions", tags=["descriptions"])


@router.post("/generate", response_model=DescriptionGenerationResponse)
async def generate_description(request: GenerateDescriptionRequest):
    """
    Generate a mystical jewelry description.

    Creates a description based on jewelry type and materials used.
    """
    try:
        logger.info(
            "Generating jewelry description",
            jewelry_type=request.jewelry_type,
            material_count=len(request.materials)
        )

        # Get description generator service
        generator = get_description_generator()

        # Convert materials to domain entities for the service
        from jewelry_description.models.entities import Material

        materials = [
            Material(name=name, unit_price=1.0, quantity=1.0, unit="шт")
            for name in request.materials
        ]

        # Generate description
        description = generator.generate_description(request.jewelry_type, materials)

        # Generate some basic hashtags
        hashtags = [
            f"#{request.jewelry_type}",
            "#handmade",
            "#jewelry",
            "#art",
        ]

        # Add material-based hashtags
        for material in request.materials[:2]:  # Limit to first 2 materials
            clean_name = material.lower().replace(" ", "").replace("-", "")
            if len(clean_name) > 0:
                hashtags.append(f"#{clean_name}")

        response = DescriptionGenerationResponse(
            description=description,
            jewelry_type=request.jewelry_type,
            material_count=len(request.materials),
            hashtags=hashtags,
        )

        logger.info(
            "Description generated successfully",
            jewelry_type=request.jewelry_type,
            description_length=len(description)
        )

        return response

    except Exception as e:
        import traceback
        logger.error(
            "Failed to generate description",
            error=str(e),
            jewelry_type=request.jewelry_type,
            traceback=traceback.format_exc()
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate jewelry description: {str(e)}"
        )