import psycopg2
from models.product_raw_entity import ProductReviewRawEntity
from models.product_clean_entity import ProductReviewCleanEntity
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
