from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from sqlalchemy.orm import sessionmaker
from app.database import Database

db = Database()
Session = db.Session

app = FastAPI(title="Amazon Product Intelligence")

class ProductInsightResponse(BaseModel):
    product_id: int
    review_count: int
    positive_percentage: float
    negative_percentage: float
    top_issues: str

@app.get("/api/v1/products/{product_id}", response_model=ProductInsightResponse)
async def get_product_insights(product_id: str):
    """
    Get insights for a specific product
    """
    session = Session()
    product_insight = session.query(ProductInsight).filter(ProductInsight.product_id == product_id).first()
    return product_insight

@app.get("/api/v1/products")
async def get_products(page: int = 1, page_size: int = 50):
    """
    Get all products with pagination
    """
    # TODO: Implement product listing
    pass