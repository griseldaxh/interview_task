from datetime import datetime
from app.models import ProductInsight
from sqlalchemy.orm import sessionmaker
from app.database import Database

Session = sessionmaker(bind=engine)

def aggregate_product_insights():
    db = Database()
    session = db.get_session()
    products = session.query(Product).all()

    for product in products:
        reviews = session.query(Review).filter(Review.product_id == product.product_id).all()
        review_count = len(reviews)
        positive_reviews = sum(1 for r in reviews if r.sentiment == "positive")
        negative_reviews = sum(1 for r in reviews if r.sentiment == "negative")
        positive_percentage = (positive_reviews / review_count) * 100
        negative_percentage = (negative_reviews / review_count) * 100

        # Find most common issues
        issues = [r.issues for r in reviews]
        top_issues = ' '.join(issues)

        insight = ProductInsight(
            product_id=product.product_id,
            review_count=review_count,
            positive_percentage=positive_percentage,
            negative_percentage=negative_percentage,
            top_issues=top_issues,
            insight_date=datetime.today().date()
        )
        session.add(insight)
    session.commit()
