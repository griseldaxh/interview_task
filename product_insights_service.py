from analyzer import ProductAnalyzer
from repository.products_repository import ProductsRepository
from models.product_insights import ProductInsights
import asyncio
import json
from logger import get_logger

logger = get_logger(__name__)

class ProductInsightsService:
    def __init__(self, product_analyzer: ProductAnalyzer, products_repository: ProductsRepository):
        self.product_analyzer = product_analyzer
        self.product_repository = products_repository

    
    async def get_insight(self, product_id: str) -> dict:
        #TODO can implement caching to reduce cost if querying product multiple times

        """
        1. TODO Check if there is a record for the product
        2. TODO get existing summary for product
        3. DONE get reviews of product then analyze
        4. TODO conolidate analysis with basic stat summaries
        """

        reviews = self.product_repository.get_product_reviews(product_id=product_id)

        # logger.info(f"TEST {reviews}")
        reviews_as_dict = [review.__dict__ for review in reviews]
        # logger.info(f"TEST {reviews_as_dict}")

        reviews_dict_json = json.dumps(reviews_as_dict, default=str)
        insights = await self.product_analyzer.analyze_reviews(reviews= reviews_dict_json)

        response = {}

        response["issue_highlights"] = insights["issue_highlights"]
        response["historical_standing"] = insights["historical_standing"]
        return insights
