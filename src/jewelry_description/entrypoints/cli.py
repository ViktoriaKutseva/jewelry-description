import typer
from jewelry_description.business.services import JewelryCostCalculator
from jewelry_description.models.entities import Material, Consumable, WorkTime

app = typer.Typer()

@app.command()
def calc(
    material_name: str,
    material_price: float,
    material_quantity: float,
    work_hours: float,
    hourly_rate: float
):
    material = Material(name=material_name, unit_price=material_price, quantity=material_quantity)
    work_time = WorkTime(hours=work_hours, hourly_rate=hourly_rate)
    calculator = JewelryCostCalculator()
    cost = calculator.calculate([material], [], work_time)
    typer.echo(f"Total cost: {cost}")

if __name__ == "__main__":
    app()
