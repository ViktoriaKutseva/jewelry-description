import typer
from ...business.services import JewelryCostCalculatorService
from ...models.entities import Material, Consumable, WorkTime, JewelryCostInput

app = typer.Typer()


@app.callback()
def main() -> None:
    """Jewelry cost calculator CLI."""
    pass


@app.command()
def calc(
    material_name: str = typer.Argument(..., help="Name of the material"),
    material_price: float = typer.Argument(..., help="Price per unit of material"),
    material_quantity: float = typer.Argument(..., help="Quantity of material"),
    work_hours: float = typer.Argument(..., help="Hours of work"),
    hourly_rate: float = typer.Argument(..., help="Hourly rate for work"),
) -> None:
    """Calculate jewelry cost with detailed breakdown."""
    # Dependency composition
    calculator = JewelryCostCalculatorService()

    material = Material(
        name=material_name, unit_price=material_price, quantity=material_quantity
    )
    work_time = WorkTime(hours=work_hours, hourly_rate=hourly_rate)

    # Standard consumables
    consumables = [
        Consumable(name="Расходники (шлифовка, воск, упаковка)", approx_cost=350),
        Consumable(name="Электричество", approx_cost=20),
        Consumable(name="Амортизация инструмента", approx_cost=125),
        Consumable(name="Цаполак (лак для металла)", approx_cost=50),
    ]

    data = JewelryCostInput(
        materials=[material], consumables=consumables, work_time=work_time
    )

    result = calculator.calculate_cost(data)

    typer.echo("=== Jewelry Cost Calculation ===")
    typer.echo(f"Total cost: {result.total_cost:.2f}")
    typer.echo()

    typer.echo("Cost Breakdown:")
    for item, cost in result.cost_breakdown.items():
        typer.echo(f"  {item}: {cost:.2f}")
    typer.echo()

    typer.echo("Recommended Selling Prices:")
    for price_type, price in result.recommended_prices.items():
        typer.echo(f"  {price_type}: {price:.2f}")
    typer.echo()

    typer.echo("💡 Recommendation:")
    typer.echo(result.price_comment)
