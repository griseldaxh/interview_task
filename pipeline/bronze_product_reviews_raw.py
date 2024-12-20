import json
from dataclasses import dataclass
from logger import get_logger
from repository.products_repository import ProductsRepository
from models.product_raw_entity import ProductReviewRawEntity
logger = get_logger(__name__)


class BronzeProductReviewsRawPipeline:
    def __init__(self, products_repository: ProductsRepository):
        self.products_repository = products_repository
    
    def reader_parse_file(self, json_file: str) -> list:
        with open(json_file, 'r') as file:
            json_array = json.load(file)
        
        products: list = []

        for product_json in json_array:
            logger.debug(f"Processing raw json: {product_json}")
            product = ProductReviewRawEntity(
                product_json["PRODUCT_BRAND"],
                product_json["CUSTOMER_REVIEW_RATING"],
                product_json["CUSTOMER_REVIEW_TITLE"],
                product_json["CUSTOMER_REVIEW_DESCRIPTION"],
                product_json["CHILD_ASIN"]
            )

            logger.debug(f"Processed json to object: {product}")
            products.append(product)
            
        return products

    def writer_insert_to_db(self, products_raw: list[ProductReviewRawEntity]):

        for product_raw in products_raw:
            self.products_repository.save_raw(product_raw)

