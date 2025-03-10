# Define main here
"""
This main.py can be used to execute the ingestion pipeline for product reviews
"""

from pipeline.bronze_product_reviews_raw import BronzeProductReviewsRawPipeline
from pipeline.silver_product_reviews_clean import SilverProductReviewsCleanPipeline
from repository.products_repository import ProductsRepository
import psycopg2
import config

conn = psycopg2.connect(
    dbname=config.POSTGRES_DB,
    user=config.POSTGRES_USERNAME,
    password=config.POSTGRES_PASSWORD,
    host="localhost",  # or your PostgreSQL host
    port="5432"        # Default PostgreSQL port
)

files = ["Interview_Products_Reviews/reviews_part_1.json", "Interview_Products_Reviews/reviews_part_2.json", "Interview_Products_Reviews/reviews_part_3.json", "Interview_Products_Reviews/reviews_part_4.json"]
repository = ProductsRepository(conn)
pipeline = BronzeProductReviewsRawPipeline(products_repository=repository)

for file in files:
    products_raw = pipeline.reader_parse_file(file)
    print(len(products_raw))
    pipeline.writer_insert_to_db(products_raw)

silver_pipeline = SilverProductReviewsCleanPipeline(products_repository=repository)

cursor = conn.cursor()
cursor.execute("SELECT * FROM bronze_product_reviews_raw")
silver_pipeline.run_pipeline(cursor)
