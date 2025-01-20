import os
import sys
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services.data_collection import DataCollector
from app.services.analyzer import ProductAnalyzer
from app.services.aggregate_insights import ProductInsightAggregator
from app.database import Database
from app.models import Review
from dotenv import load_dotenv

async def main():
    """Main application logic separated from entry point."""
    database_url, openai_api_key = load_config()
    
    # Initialize components
    processor = DataCollector()
    analyzer = ProductAnalyzer(api_key=openai_api_key)
    db = Database()
    session = db.get_session()
    
    try:
        # Process files and analyze reviews
        await process_pipeline(processor, analyzer, session)
    finally:
        session.close()

async def process_pipeline(processor: DataCollector, analyzer: ProductAnalyzer, session) -> None:
    """Execute the complete processing pipeline."""
    try:
        process_mockup_files(processor)
        await analyze_reviews(analyzer, session)
                
        aggregator = ProductInsightAggregator()
        aggregator.aggregate_insights()
    except Exception as e:
        print(f"Pipeline error: {str(e)}")
        raise

def load_config() -> tuple[str, str]:
    """Load and return configuration from environment variables."""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not database_url or not openai_api_key:
        raise ValueError("Missing required environment variables: DATABASE_URL and/or OPENAI_API_KEY")
    
    return database_url, openai_api_key

def process_mockup_files(processor: DataCollector) -> None:
    """Process all JSON files in the mockup directory.
    
    Args:
        processor: DataCollector instance to handle the file processing
    """
    mockup_dir = './mockup'
    json_files = glob.glob(os.path.join(mockup_dir, '*.json'))
    
    if not json_files:
        print("No JSON files found in mockup directory")
        return
    
    for file_path in json_files:
        try:
            print(f"Processing file: {file_path}")
            processor.preprocess_and_store_data(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

async def analyze_reviews(analyzer: ProductAnalyzer, db_session) -> None:
    """Analyze all unprocessed reviews in the database in batches."""
    # Query reviews that don't have sentiment analysis yet
    reviews = db_session.query(Review).filter(
        (Review.sentiment == '') | (Review.sentiment.is_(None))
    ).all()
    
    if not reviews:
        print("No reviews to analyze")
        return
    
    BATCH_SIZE = 200  # Adjust this value based on your needs
    total_reviews = len(reviews)
    print(f"Analyzing {total_reviews} reviews in batches of {BATCH_SIZE}...")
    
    for i in range(0, total_reviews, BATCH_SIZE):
        batch = reviews[i:i + BATCH_SIZE]
        review_data = [
            {
                'review_id': review.review_id,
                'review_title': review.review_title,
                'review_description': review.review_description,
                'rating': review.rating
            }
            for review in batch
        ]
        
        analyzed_reviews = await analyzer.analyze_reviews_batch(review_data)
        
        # Update reviews with analysis results
        for analyzed in analyzed_reviews:
            review = next(r for r in batch if r.review_id == analyzed['review_id'])
            review.sentiment = analyzed['sentiment']
            review.issues = analyzed['issues']
        
        db_session.commit()
        print(f"Processed batch {i//BATCH_SIZE + 1}/{(total_reviews + BATCH_SIZE - 1)//BATCH_SIZE}")
    
    print("Review analysis completed")

if __name__ == "__main__":
    """Main application entry point."""
    import asyncio
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Application error: {str(e)}")
        sys.exit(1)
