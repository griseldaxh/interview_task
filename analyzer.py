from typing import Dict, List
import json
from logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """
    You are a market analyzer with the task of consolidating product reviews of a product you sell.
    You will be given multiple reviews of the products including the rating given from the review, and when the review was made, with
    a rating of 1 being the lowest and rating 5 the highest. 

    You must provide the following output after analyzing the product reviews:
    
    issue_highlights - a list of issues most shared among the negative reviews
    historical_standing - a summary of how the product has fared given its past performances, include the timestamp in your analysis

    Your output must be in the json format of:
    {
        "issue_highlights": array of string
        "historical_standing": string
    }

    YOU MUST OUTPUT YOUR ANSWER DIRECTLY AND IT MUST BE A VALID JSON
    """

class ProductAnalyzer:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def analyze_reviews(self, reviews: List[Dict]) -> Dict:
        """
        Analyze product reviews using LLM to extract insights
        """

        """
        Steps for analyze_reviews:
        1. check if existing insights have been made
        2. if not, generate new insight
        2.1 get basic summary
        2.2 get all product reviews
        2.3 use llm to 
        """
        response = self.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": reviews},
            ]
        )
        json_response = response.choices[0].message.content
        logger.info(f"Retrieved raw ressponse from ChatGPT: {json_response}")

        response_as_dict = eval(json_response)
        logger.info(f"Retrieved analysis from ChatGPT: {response_as_dict}")
        return response_as_dict

    