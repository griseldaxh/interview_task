from typing import Dict, List
import openai
import asyncio

class ProductAnalyzer:
    def __init__(self, api_key, llm_client=None):
        openai.api_key = api_key
        self.llm_client = llm_client or openai

    async def analyze_reviews_batch(self, reviews: List[Dict]) -> List[Dict]:
        """
        Analyze all product reviews in parallel for maximum performance.
        """
        # Process all reviews at once
        batch_results = await asyncio.gather(
            *[self._analyze_review_with_llm(review['review_description'])
              for review in reviews]
        )

        # Combine results with original review data
        results = [
            {
                'review_id': review['review_id'],
                'review_title': review['review_title'],
                'rating': review['rating'],
                'review_description': review['review_description'],
                'sentiment': analysis['sentiment'],
                'issues': analysis['issues'],
            }
            for review, analysis in zip(reviews, batch_results)
        ]

        return results

    async def _analyze_review_with_llm(self, review_text: str) -> Dict:
        """
        Helper function to analyze the review text using the LLM client (OpenAI Chat Completions).
        """
        prompt = """Analyze the following product review and provide a structured response with:
1. Sentiment analysis (positive/negative/neutral)
2. List of issues or concerns (if any)

Review: {review_text}

Format your response as:
Sentiment: [sentiment]
Issues: [list issues or "None" if no issues found]"""

        response = self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes product reviews."},
                {"role": "user", "content": prompt.format(review_text=review_text)},
            ],
            max_tokens=150,
            temperature=0.3,
        )

        analysis = response.choices[0].message.content.strip()
        sentiment = self._extract_sentiment_from_structured(analysis)
        issues = self._extract_issues_from_structured(analysis)

        return {'sentiment': sentiment, 'issues': issues}

    def _extract_sentiment_from_structured(self, analysis: str) -> str:
        """
        Extract sentiment from structured LLM analysis.
        Returns 'positive', 'negative', or 'neutral'.
        """
        for line in analysis.split('\n'):
            if line.lower().startswith('sentiment:'):
                sentiment = line.split(':', 1)[1].strip().lower()
                return sentiment if sentiment in ['positive', 'negative', 'neutral'] else 'neutral'
        return 'neutral'

    def _extract_issues_from_structured(self, analysis: str) -> List[str]:
        """
        Extract list of issues from structured LLM analysis.
        Returns a list of identified issues.
        """
        for line in analysis.split('\n'):
            if line.lower().startswith('issues:'):
                issues_text = line.split(':', 1)[1].strip()
                if issues_text.lower() in ['none', 'no issues']:
                    return
                return [issue.strip() for issue in issues_text.split(',')]
        return
