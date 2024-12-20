from pydantic import BaseModel
from datetime import datetime

class ProductSummary(BaseModel):
    child_asin: str
    no_of_reviews: int
    average_rating: float
    max_rating: int
    min_rating: int

class ProductReview(BaseModel):
    product_brand: str
    customer_review_rating: int
    customer_review_title: str
    customer_review_description: str
    child_asin: str
    created_at_ts: datetime
    updated_at_ts: datetime
    ingested_at_ts: datetime

class ProductInsightResponse(BaseModel):
    child_asin: str
    no_of_reviews: int
    average_rating: float
    max_rating: int
    min_rating: int
    issue_highlight: list[str]
    historical_standing: str