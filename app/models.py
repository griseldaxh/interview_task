from sqlalchemy import Column, Integer, String, Float, Date, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    asin = Column(String, unique=True, nullable=False)
    brand = Column(String)

    reviews = relationship("Review", back_populates="product")
    insights = relationship("ProductInsight", back_populates="product")


class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    review_title = Column(String)
    review_description = Column(String)
    rating = Column(Integer)
    sentiment = Column(String)
    issues = Column(String)

    product = relationship("Product", back_populates="reviews")


class ProductInsight(Base):
    __tablename__ = 'product_insights'

    insight_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    review_count = Column(Integer)
    positive_percentage = Column(Float)
    negative_percentage = Column(Float)
    top_issues = Column(String)
    insight_date = Column(Date)
    version = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("Product", back_populates="insights")
