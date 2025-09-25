from typing import List, Dict, Any
from loguru import logger

from jewelry_description.models.entities import Material, Consumable, WorkTime


class JewelryCostCalculator:
    """Service for calculating jewelry costs."""
    
    def calculate(
        self, 
        materials: List[Material], 
        consumables: List[Consumable], 
        work_time: WorkTime, 
        electricity_cost: float = 0.0, 
        tool_depreciation: float = 0.0, 
        packaging_cost: float = 0.0, 
        extra_costs: List[Consumable] | None = None, 
        defect_percent: float = 0.0
    ) -> float:
        """Calculate total cost for jewelry production."""
        
        if extra_costs is None:
            extra_costs = []
            
        logger.info(
            "Calculating jewelry cost",
            materials_count=len(materials),
            consumables_count=len(consumables),
            work_hours=work_time.hours,
            hourly_rate=work_time.hourly_rate
        )
        
        material_cost = sum(m.cost() for m in materials)
        consumable_cost = sum(c.approx_cost for c in consumables)
        extra_cost = sum(c.approx_cost for c in extra_costs)
        work_cost = work_time.cost()
        
        total = (
            material_cost + 
            consumable_cost + 
            work_cost + 
            electricity_cost + 
            tool_depreciation + 
            packaging_cost + 
            extra_cost
        )
        
        if defect_percent > 0:
            total *= (1 + defect_percent / 100)
            
        logger.info(
            "Cost calculation completed",
            material_cost=material_cost,
            work_cost=work_cost,
            total_cost=total
        )
        
        return total


class WebJewelryCostService:
    """Service for web-specific jewelry cost calculations."""
    
    def __init__(self, calculator: JewelryCostCalculator):
        self.calculator = calculator
    
    def calculate_with_recommendations(
        self, 
        materials: List[Dict[str, Any]], 
        hours: float, 
        hourly_rate: float
    ) -> Dict[str, Any]:
        """
        Calculate jewelry cost with price recommendations for web interface.
        
        Args:
            materials: List of dicts with {"name": str, "quantity": float, "price": float, "unit": str}
            hours: Work hours
            hourly_rate: Hourly rate in KZT
        
        Returns:
            Dict with total_cost, recommended_prices, and price_comment
        """
        logger.info("Starting web cost calculation", material_count=len(materials))
        
        # Convert web format to business logic format
        material_objects = []
        for mat in materials:
            material_obj = Material(
                name=mat["name"],
                unit_price=mat["price"],
                quantity=mat["quantity"],
                unit=mat.get("unit", "г")
            )
            material_objects.append(material_obj)
        
        # Standard consumables (as used in example_usage.py)
        consumables = [
            Consumable(name="Расходники (шлифовка, воск, упаковка)", approx_cost=350),
            Consumable(name="Электричество", approx_cost=20),
            Consumable(name="Амортизация инструмента", approx_cost=125),
            Consumable(name="Цаполак (лак для металла)", approx_cost=50),
        ]
        
        work_time = WorkTime(hours=hours, hourly_rate=hourly_rate)
        
        # Calculate using existing business logic
        total_cost = self.calculator.calculate(material_objects, consumables, work_time)
        
        # Calculate recommended prices
        recommended_prices = {
            "minimal": total_cost * 2,
            "comfortable": total_cost * 2.5,
            "premium": total_cost * 3
        }
        
        # Create price comment
        min_price = int(recommended_prices["minimal"] * 1.1)
        comfort_price = int(recommended_prices["comfortable"] * 1.1)
        price_comment = (
            f"👉 Отличная розничная цена: от {min_price:,} до {comfort_price:,} ₸, "
            f"в зависимости от упаковки и позиционирования."
        ).replace(",", " ")
        
        result = {
            "total_cost": total_cost,
            "recommended_prices": recommended_prices,
            "price_comment": price_comment
        }
        
        logger.info("Web cost calculation completed", total_cost=total_cost)
        return result
