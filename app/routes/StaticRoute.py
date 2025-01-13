from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from fastapi import Depends
from ..routes.ProductRoute import get_products

router = APIRouter(prefix="", tags=["html"])

# Route to serve the HTML file at the root ("/")
@router.get("/")
async def get_html():
    # Read the static HTML file from the correct location
    try:
        static_dir = Path(__file__).parent.parent / "static"
        with open(static_dir / "index.html") as f:
            html_content = f.read()
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

    # Return the modified HTML content
    return HTMLResponse(content=html_content, status_code=200)
