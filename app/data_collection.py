import json
from sqlalchemy.orm import sessionmaker
from models import Product, Review
from database import engine

Session = sessionmaker(bind=engine)

def load_product_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def preprocess_and_store_data(file_path):
    data = load_product_data(file_path)
    session = Session()

    for product_data in data:
        # Check if product already exists
        existing_product = session.query(Product).filter_by(asin=product_data['CHILD_ASIN']).first()
        
        if existing_product:
            product = existing_product
        else:
            product = Product(asin=product_data['CHILD_ASIN'], brand=product_data['PRODUCT_BRAND'])
            session.add(product)
            session.commit()

        # Add reviews for this product
        review_obj = Review(
            product_id=product.product_id,
            review_title=product_data['CUSTOMER_REVIEW_TITLE'],
            review_description=product_data['CUSTOMER_REVIEW_DESCRIPTION'],
            rating=product_data['CUSTOMER_REVIEW_RATING'],
            sentiment='',  # Sentiment will be analyzed next
            issues=[]  # Issues will be identified later
        )
        session.add(review_obj)
        session.commit()

# Example usage
file_path = './mockup/reviews_part_1.json'  # Update with the path to your JSON file
preprocess_and_store_data(file_path)