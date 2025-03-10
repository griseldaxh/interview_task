import psycopg2
from psycopg2 import sql
from models.product_raw_entity import ProductReviewRawEntity
from models.product_clean_entity import ProductReviewCleanEntity
from models.product_summary_entity import ProductSummaryEntity
from logger import get_logger

logger = get_logger(__name__)
class ProductsRepository:
    def __init__(self, conn):
        self.conn = conn

    def save_raw(self, entity: ProductReviewRawEntity):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO bronze_product_reviews_raw (product_brand, customer_review_rating, customer_review_title, customer_review_description, child_asin)
            VALUES (%s, %s, %s, %s, %s)
        ''', (entity.product_brand, 
              entity.customer_review_rating, entity.customer_review_title, entity.customer_review_description, entity.child_asin))
        
        self.conn.commit()

    def save_clean(self, entity: ProductReviewCleanEntity):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO silver_product_reviews_clean (product_brand, customer_review_rating, customer_review_title, customer_review_description, child_asin, created_at_ts, updated_at_ts, ingested_at_ts)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (entity.product_brand, 
              entity.customer_review_rating, entity.customer_review_title, entity.customer_review_description, entity.child_asin, entity.created_at_ts, entity.updated_at_ts, entity.ingested_at_ts))
        
        self.conn.commit()

    def get_product_reviews(self, product_id: str) -> list[ProductReviewCleanEntity]:
        logger.info(f"Retrieving all reviews for {product_id}")
        cursor = self.conn.cursor()
        query = sql.SQL('''
            select *
            from silver_product_reviews_clean
            where child_asin = %s
        ''')

        cursor.execute(query, (product_id,))
        
        records = cursor.fetchall()

        product_summaries = []
        if records:
            logger.info(f"Retrieved {len(records)} recrods")
            for record in records:
                product_summary = ProductReviewCleanEntity(*record)
                logger.debug(f"RETRIEVED {product_summary.__dict__}")
                product_summaries.append(product_summary)

            return product_summaries
        else:
            logger.error(f"No products retrieved from database")
            return None
    
    def get_products_summary(self, page: int, page_size:int) -> list[ProductSummaryEntity]:
        """
        Paginated implementation for getting summarized insights of multiple products. 
        We use the limit-offset functionality for simplicity
        """
        logger.info(f"Retrieving product summary data for page: {page} with page_size: {page_size}")
        offset = int(page * page_size)
        cursor = self.conn.cursor()
        query = sql.SQL('''
            SELECT *
            FROM gold_product_summary
            ORDER BY child_asin
            LIMIT %s
            OFFSET %s
        ''')

        cursor.execute(query, (page_size, offset))
        
        records = cursor.fetchall()

        product_summaries = []
        if records:
            logger.info(f"Retrieved {len(records)} recrods")
            for record in records:
                product_summary = ProductSummaryEntity(*record)
                logger.debug(f"RETRIEVED {product_summary.__dict__}")
                product_summaries.append(product_summary)

            return product_summaries
        else:
            logger.error(f"No products retrieved from database")
            return None

