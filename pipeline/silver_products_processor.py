from models.product_clean_entity import ProductReviewCleanEntity
from models.product_raw_entity import ProductReviewRawEntity
from datetime import datetime
import time
import random

def generate_random_timestamp():
    current_time = time.time()
    one_year_ago = current_time - (365 * 24 * 60 * 60)
    random_epoch = random.uniform(one_year_ago, current_time)
    random_datetime = datetime.fromtimestamp(random_epoch)
    return random_datetime

def process(entity: ProductReviewRawEntity) -> ProductReviewCleanEntity:

    random_timestamp = generate_random_timestamp()
    clean_entity = ProductReviewCleanEntity(
        product_brand=entity.product_brand,
        customer_review_rating=int(entity.customer_review_rating),
        customer_review_title=entity.customer_review_title,
        customer_review_description=entity.customer_review_description,
        child_asin=entity.child_asin,
        created_at_ts=random_timestamp,
        updated_at_ts=random_timestamp,
        ingested_at_ts=datetime.now()
    )

    return clean_entity