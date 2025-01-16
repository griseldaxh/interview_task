import openai

openai.api_key = "your-api-key"

def analyze_sentiment_and_issues(review_text):
    prompt = f"Extract sentiment and issues from the following review: {review_text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def analyze_reviews(session):
    reviews = session.query(Review).all()
    for review in reviews:
        sentiment = analyze_sentiment_and_issues(review.review_description)
        review.sentiment = sentiment
        session.commit()
