from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from fastapi import Depends
from ..routes.ProductRoute import get_products

router = APIRouter(prefix="", tags=["html"])

# Route to serve the HTML file at the root ("/")
@router.get("/", response_class=HTMLResponse)
async def get_html(db: AsyncSession = Depends(get_db)):
    # Get products from the repository
    products = await get_products(db)
    
    # Build product items dynamically
    product_items = ""
    for product in products:
        product_item = f"""
        <div class="product-item">
            <img src="{ 'https://via.placeholder.com/200'}" alt="Product Image">
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p class="price">${product.price}</p>
        </div>
        """
        product_items += product_item

    # Read the static HTML file from the correct location
    try:
        static_dir = Path(__file__).parent.parent / "static"
        with open(static_dir / "index.html") as f:
            html_content = f.read()
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

    # Replace the placeholder with the actual product items
    html_content = html_content.replace("{product_items}", product_items)
    
    # Return the modified HTML content
    return HTMLResponse(content=html_content, status_code=200)
