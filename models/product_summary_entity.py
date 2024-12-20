from dataclasses import dataclass

@dataclass
class ProductSummaryEntity():
    def __init__(self, 
                 child_asin: str,
                 no_of_reviews: int,
                 average_rating: float,
                 max_rating: int,
                 min_rating: int
                 ):
        self.child_asin = child_asin
        self.no_of_reviews = no_of_reviews
        self.average_rating = average_rating
        self.max_rating = max_rating
        self.min_rating = min_rating