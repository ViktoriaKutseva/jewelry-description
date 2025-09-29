"""
Calculator API endpoints.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from loguru import logger

from ..dependencies import get_cost_calculator
from ..schemas import (
    CalculateCostRequest,
    CostCalculationResponse,
    PriceRecommendations,
    CalculationMetadata,
)


router = APIRouter(prefix="/api/v1/calculator", tags=["calculator"])


@router.post("/calculate", response_model=CostCalculationResponse)
async def calculate_cost(request: CalculateCostRequest):
    """
    Calculate jewelry production cost with recommendations.

    Takes material list, jewelry specifications, and pricing parameters,
    returns total cost breakdown and recommended selling prices.
    """
    try:
        logger.info(
            "Calculating jewelry cost",
            jewelry_type=request.jewelry_type,
            material_count=len(request.materials),
            weight=request.weight
        )

        # Get calculator service
        calculator = get_cost_calculator()

        # Convert request to domain entities
        from jewelry_description.models.entities import (
            Material,
            WorkTime,
            JewelryCostInput,
            Consumable,
        )

        materials = [
            Material(
                name=m.name,
                unit_price=m.unit_price,
                quantity=m.quantity,
                unit=m.unit
            )
            for m in request.materials
        ]

        # Calculate work time based on weight and complexity
        complexity_multipliers = {
            "simple": 1.0,
            "medium": 1.5,
            "complex": 2.0,
            "very_complex": 3.0
        }
        
        base_hours_per_gram = 0.1  # Base work time per gram
        complexity_multiplier = complexity_multipliers.get(request.complexity, 1.5)
        estimated_hours = request.weight * base_hours_per_gram * complexity_multiplier
        
        # Use labor cost as hourly rate
        hourly_rate = request.labor_cost / max(estimated_hours, 1.0) if request.labor_cost > 0 else 50.0

        work_time = WorkTime(
            hours=estimated_hours,
            hourly_rate=hourly_rate
        )

        # Create consumables based on options
        consumables = []
        if request.include_gemstones:
            consumables.append(Consumable(name="Gemstone settings", approx_cost=request.weight * 10))
        if request.include_findings:
            consumables.append(Consumable(name="Findings and clasps", approx_cost=request.weight * 5))

        # Quality adjustment
        quality_multipliers = {
            "standard": 1.0,
            "premium": 1.2,
            "luxury": 1.5
        }
        quality_multiplier = quality_multipliers.get(request.quality, 1.2)

        # Create input for calculation
        cost_input_data = {
            "materials": materials,
            "work_time": work_time,
            "consumables": consumables,
            "extra_costs": [],
        }

        cost_input = JewelryCostInput(**cost_input_data)

        # Perform calculation
        result = calculator.calculate_cost(cost_input)

        # Apply quality multiplier and markup
        base_cost = result.total_cost * quality_multiplier
        markup_amount = base_cost * (request.markup / 100)
        final_cost = base_cost + markup_amount

        # Update cost breakdown
        updated_breakdown = result.cost_breakdown.copy()
        updated_breakdown["Quality adjustment"] = result.total_cost * (quality_multiplier - 1)
        updated_breakdown["Markup"] = markup_amount

        # Calculate recommended prices based on final cost
        min_price = final_cost * 2
        comfort_price = final_cost * 2.5
        premium_price = final_cost * 3

        recommended_prices = PriceRecommendations(
            minimum=min_price,
            comfort=comfort_price,
            premium=premium_price,
        )

        # Create price comment
        price_comment = (
            f"Recommended retail price range: {int(min_price)} - {int(comfort_price)} ₸ "
            f"based on {request.markup}% markup and {request.quality} quality."
        )

        metadata = CalculationMetadata(
            material_count=len(request.materials),
            has_consumables=len(consumables) > 0,
            has_extra_costs=False,
            defect_percentage=None,
            calculation_timestamp=datetime.now().isoformat(),
        )

        response = CostCalculationResponse(
            total_cost=final_cost,
            cost_breakdown=updated_breakdown,
            recommended_prices=recommended_prices,
            price_comment=price_comment,
            calculation_metadata=metadata,
        )

        logger.info(
            "Cost calculation completed",
            total_cost=final_cost,
            jewelry_type=request.jewelry_type
        )

        return response

    except Exception as e:
        import traceback
        logger.error(
            "Failed to calculate cost",
            error=str(e),
            jewelry_type=request.jewelry_type,
            traceback=traceback.format_exc()
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate jewelry cost: {str(e)}"
        )