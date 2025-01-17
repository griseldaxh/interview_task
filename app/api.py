from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from typing import List
from app.database import Database
from app.models import ProductInsight

# Create a session
db = Database()
Session = db.Session

# Initialize FastAPI app
app = FastAPI(title="Amazon Product Intelligence")

# Response model using Pydantic to format the data
class ProductInsightResponse(BaseModel):
    product_id: int
    review_count: int
    positive_percentage: float
    negative_percentage: float
    top_issues: str

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models like dictionaries

@app.get("/api/v1/products/{product_id}", response_model=ProductInsightResponse)
async def get_product_insights(product_id: int):
    """
    Get insights for a specific product based on product_id.
    """
    session = Session()
    product_insight = session.query(ProductInsight).filter(ProductInsight.product_id == product_id).first()

    # If no insights are found, raise an HTTPException
    if not product_insight:
        raise HTTPException(status_code=404, detail="Product not found or no insights available.")

    return product_insight

@app.get("/api/v1/products", response_model=List[ProductInsightResponse])
async def get_products(page: int = 1, page_size: int = 50):
    """
    Get a list of products with pagination.
    """
    session = Session()
    offset = (page - 1) * page_size
    products = session.query(ProductInsight).offset(offset).limit(page_size).all()

    # If no products are found, raise an HTTPException
    if not products:
        raise HTTPException(status_code=404, detail="No products found.")
    
    return products
