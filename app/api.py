from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from typing import List
from app.database import Database
from app.models import ProductInsight, Product, Review

# Create a session
db = Database()
Session = db.Session

# Initialize FastAPI app
app = FastAPI(title="Amazon Product Intelligence")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Response model using Pydantic to format the data
class ProductInsightResponse(BaseModel):
    product_id: int
    review_count: int
    positive_percentage: float
    negative_percentage: float
    top_issues: str

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models like dictionaries

class ProductReviewResponse(BaseModel):
    product_id: int
    product_asin: str
    product_brand: str
    reviews: List[dict]  # This will contain individual reviews

    class Config:
        orm_mode = True

class CombinedProductResponse(BaseModel):
    product_id: int
    asin: str
    brand: str
    review_count: int
    positive_percentage: float
    negative_percentage: float
    top_issues: str

    class Config:
        orm_mode = True

class ProductsListResponse(BaseModel):
    total: int
    products: List[CombinedProductResponse]

    class Config:
        orm_mode = True

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

@app.get("/api/v1/products", response_model=ProductsListResponse)
async def get_products(page: int = 1, page_size: int = 50):
    """
    Get a list of products with their insights, including pagination and total count.
    """
    session = Session()
    offset = (page - 1) * page_size
    
    # Get total count of products with insights
    total_products = session.query(Product)\
        .join(ProductInsight)\
        .count()
    
    # Get paginated products with insights
    products = session.query(
        Product.product_id,
        Product.asin,
        Product.brand,
        ProductInsight.review_count,
        ProductInsight.positive_percentage,
        ProductInsight.negative_percentage,
        ProductInsight.top_issues
    )\
        .join(ProductInsight)\
        .offset(offset)\
        .limit(page_size)\
        .all()

    # If no products are found, raise an HTTPException
    if not products:
        raise HTTPException(status_code=404, detail="No products found.")
    
    # Convert the query results to dictionaries
    product_list = [
        {
            "product_id": p.product_id,
            "asin": p.asin,
            "brand": p.brand,
            "review_count": p.review_count,
            "positive_percentage": p.positive_percentage,
            "negative_percentage": p.negative_percentage,
            "top_issues": p.top_issues
        } for p in products
    ]
    
    return {
        "total": total_products,
        "products": product_list
    }

@app.get("/api/v1/product/{product_id}", response_model=ProductReviewResponse)
async def get_product_details(product_id: int):
    """
    Get complete product details including all reviews for a specific product.
    """
    session = Session()
    
    # Query for product details and reviews
    product = session.query(Product).filter(Product.product_id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    reviews = session.query(Review).filter(Review.product_id == product_id).all()
    
    return {
        "product_id": product.product_id,
        "product_asin": product.asin,
        "product_brand": product.brand,
        "reviews": [
            {
                "review_id": review.review_id,
                "review_title": review.review_title,
                "review_description": review.review_description,
                "rating": review.rating,
            } for review in reviews
        ],
        "total_reviews": len(reviews)
    }
