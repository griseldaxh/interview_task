from datetime import datetime
from app.models import ProductInsight, Product, Review
from sqlalchemy.orm import sessionmaker
from app.database import Database

class ProductInsightAggregator:
    def __init__(self):
        self.db = Database()
        self.session = self.db.get_session()

    def aggregate_insights(self):
        products = self.session.query(Product).all()
        
        for product in products:
            insight = self._create_product_insight(product)
            self.session.add(insight)
        
        self.session.commit()

    def _create_product_insight(self, product):
        reviews = self._get_product_reviews(product)
        review_count = len(reviews)
        
        sentiment_stats = self._calculate_sentiment_stats(reviews, review_count)
        top_issues = self._get_top_issues(reviews)

        return ProductInsight(
            product_id=product.product_id,
            review_count=review_count,
            positive_percentage=sentiment_stats['positive'],
            negative_percentage=sentiment_stats['negative'],
            top_issues=top_issues,
            insight_date=datetime.today().date()
        )

    def _get_product_reviews(self, product):
        return self.session.query(Review).filter(
            Review.product_id == product.product_id
        ).all()

    def _calculate_sentiment_stats(self, reviews, review_count):
        positive_reviews = sum(1 for r in reviews if r.sentiment == "positive")
        negative_reviews = sum(1 for r in reviews if r.sentiment == "negative")
        
        return {
            'positive': positive_reviews,
            'negative': negative_reviews
        }

    def _get_top_issues(self, reviews):
        issues = []
        for review in reviews:
            if isinstance(review.issues, list):
                issues.extend(review.issues)
            else:
                issues.append(review.issues)
        return '; '.join(filter(None, issues))
