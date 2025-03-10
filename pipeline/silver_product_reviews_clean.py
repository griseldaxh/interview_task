import json
from logger import get_logger
from repository.products_repository import ProductsRepository
from models.product_clean_entity import ProductReviewCleanEntity
from models.product_raw_entity import ProductReviewRawEntity
from .silver_products_processor import process
logger = get_logger(__name__)


class SilverProductReviewsCleanPipeline:
    def __init__(self, products_repository: ProductsRepository):
        self.products_repository = products_repository
    

    def reader_parse_product_raw(self, products_raw_cursor) -> list[ProductReviewRawEntity]:
        products_raw = []
        records = products_raw_cursor.fetchall()
        for record in records:
            product_raw = ProductReviewRawEntity(
                product_brand=record[0],
                customer_review_rating=record[1],
                customer_review_title=record[2],
                customer_review_description=record[3],
                child_asin=record[4]
            )
            products_raw.append(product_raw)
        
        return products_raw
    
    def processor_clean_raw_entity(self, products_raw: list[ProductReviewRawEntity]) -> list[ProductReviewCleanEntity]:
        products_clean = []
        for product_raw in products_raw:
            product_clean = process(product_raw)
            products_clean.append(product_clean)
        
        return products_clean


    def writer_insert_to_db(self, products_clean: list[ProductReviewCleanEntity]):

        for product_raw in products_clean:
            self.products_repository.save_clean(product_raw)
    
    def run_pipeline(self, products_raw_cursor):
        logger.info("Initiated ingestion to silver products review table.")
        products_raw = self.reader_parse_product_raw(products_raw_cursor)
        products_clean = self.processor_clean_raw_entity(products_raw)
        self.writer_insert_to_db(products_clean)
        logger.info("Completed ingestion to silver products review table.")

