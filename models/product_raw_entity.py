from dataclasses import dataclass

@dataclass
class ProductReviewRawEntity:
    def __init__(self, 
                 product_brand: str,
                 customer_review_rating: str,
                 customer_review_title: str,
                 customer_review_description: str,
                 child_asin: str):
        self.product_brand = product_brand
        self.customer_review_rating = customer_review_rating
        self.customer_review_title = customer_review_title
        self.customer_review_description = customer_review_description
        self.child_asin = child_asin