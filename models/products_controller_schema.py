from pydantic import BaseModel

class ProductSummary(BaseModel):
    child_asin: str
    no_of_reviews: int
    average_rating: float
    max_rating: int
    min_rating: int