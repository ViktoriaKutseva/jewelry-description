from models.entities import CalculationInput, CalculationResult

def calculate_jewelry_price(data: CalculationInput) -> CalculationResult:
    # ... implement your calculation logic here ...
    # Example stub:
    total_materials = sum(m.unit_price * m.quantity for m in data.materials)
    total_consumables = sum(c.approx_cost for c in data.consumables)
    work_cost = data.work_time.hours * data.work_time.hourly_rate
    total_cost = (
        total_materials +
        total_consumables +
        work_cost +
        data.electricity_cost +
        data.tool_depreciation +
        data.packaging_cost
    )
    # Apply defect percent
    total_cost *= (1 + data.defect_percent / 100)
    recommended_price = total_cost * 1.5  # Example markup
    price_comment = "Recommended price includes materials, labor, and markup."
    instagram_description = f"{data.jewelry_meta.type} in {data.jewelry_meta.style} style, size {data.jewelry_meta.size}."
    return CalculationResult(
        total_cost=total_cost,
        recommended_price=recommended_price,
        price_comment=price_comment,
        instagram_description=instagram_description
    )