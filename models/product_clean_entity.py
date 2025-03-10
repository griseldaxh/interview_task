from dataclasses import dataclass
from datetime import datetime
@dataclass
class ProductReviewCleanEntity:
    def __init__(self, 
                 product_brand: str,
                 customer_review_rating: int,
                 customer_review_title: str,
                 customer_review_description: str,
                 child_asin: str,
                 created_at_ts: datetime.tzinfo,
                 updated_at_ts: datetime.tzinfo,
                 ingested_at_ts: datetime.tzinfo):
        self.product_brand = product_brand
        self.customer_review_rating = customer_review_rating
        self.customer_review_title = customer_review_title
        self.customer_review_description = customer_review_description
        self.child_asin = child_asin
        self.created_at_ts = created_at_ts
        self.updated_at_ts = updated_at_ts
        self.ingested_at_ts = ingested_at_ts