#!/bin/bash

echo "🏺 Jewelry Calculator - Different Ways to Run"
echo "=============================================="
echo
echo "1. Using uv (Recommended):"
echo "   uv run jewelry-web"
echo
echo "2. Using uv with module:"
echo "   uv run -m jewelry_description.entrypoints.web.main"
echo
echo "3. Using Python startup script:"
echo "   python scripts/run_web.py"
echo
echo "4. Using virtual environment directly:"
echo "   .venv/bin/python -m jewelry_description.entrypoints.web.main"
echo
echo "5. Running with uvicorn directly (advanced):"
echo "   uv run uvicorn jewelry_description.entrypoints.web.main:app --host 0.0.0.0 --port 8000"
echo
echo "All methods will start the server at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"