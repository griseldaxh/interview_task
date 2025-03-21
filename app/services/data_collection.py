import json
from sqlalchemy.orm import sessionmaker
from app.models import Product, Review
import glob
import os
from app.database import Database

class DataCollector:
    def __init__(self):
        db = Database()
        self.session = db.get_session()

    def load_product_data(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def process_product(self, product_data):
        # Check if product already exists
        existing_product = self.session.query(Product).filter_by(asin=product_data['CHILD_ASIN']).first()
        
        if existing_product:
            product = existing_product
        else:
            product = Product(asin=product_data['CHILD_ASIN'], brand=product_data['PRODUCT_BRAND'])
            self.session.add(product)
            self.session.commit()

        return product

    def add_review(self, product, product_data):
        review_obj = Review(
            product_id=product.product_id,
            review_title=product_data['CUSTOMER_REVIEW_TITLE'],
            review_description=product_data['CUSTOMER_REVIEW_DESCRIPTION'],
            rating=product_data['CUSTOMER_REVIEW_RATING'],
            sentiment='',  # Sentiment will be analyzed next
            issues=[]  # Issues will be identified later
        )
        self.session.add(review_obj)
        self.session.commit()

    def preprocess_and_store_data(self, file_path):
        data = self.load_product_data(file_path)
        
        for product_data in data:
            product = self.process_product(product_data)
            self.add_review(product, product_data)
