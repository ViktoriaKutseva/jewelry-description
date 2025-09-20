from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from jewelry_description.models.entities import CalculationInput, CalculationResult
from jewelry_description.business.services import calculate_jewelry_price

app = FastAPI()

# Serve static files (JS, CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# GET / — serve HTML page
@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("app/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

# GET /api/materials — return materials from CSV/JSON
@app.get("/api/materials")
async def get_materials():
    # Example: load from CSV or JSON file
    import json
    try:
        with open("materials.json", "r", encoding="utf-8") as f:
            materials = json.load(f)
        logger.info("Loaded materials")
        return materials
    except Exception as e:
        logger.error(f"Failed to load materials: {e}")
        return []

# POST /api/calculate — accepts JSON, returns calculation result
@app.post("/api/calculate", response_model=CalculationResult)
async def calculate(data: CalculationInput):
    logger.info("Received calculation request")
    result = calculate_jewelry_price(data)
    return result

# POST /api/export_md — returns generated Markdown file (optional)
@app.post("/api/export_md")
async def export_md(data: CalculationInput):
    result = calculate_jewelry_price(data)
    md = f"# Jewelry Description\n\n{result.instagram_description}\n\n**Total Cost:** {result.total_cost}\n**Recommended Price:** {result.recommended_price}\n\n{result.price_comment}"
    return Response(content=md, media_type="text/markdown")