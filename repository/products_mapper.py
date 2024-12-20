from models.product_summary_entity import ProductSummaryEntity
from models.products_controller_schema import ProductSummary, ProductReview, ProductInsightResponse
from models.product_clean_entity import ProductReviewCleanEntity
from models.product_insights import ProductInsights
def map_to_response(product_summaries: list[ProductSummaryEntity]) -> list[ProductSummary]:

    response = []

    for product_summary in product_summaries:
        response_product_summary = ProductSummary(**product_summary.__dict__)
        response.append(response_product_summary)
    return response


def map_to_response(product_summaries: list[ProductReviewCleanEntity]) -> list[ProductReview]:

    response = []

    for product_summary in product_summaries:
        response_product_summary = ProductReview(**product_summary.__dict__)
        response.append(response_product_summary)
    return response

def map_to_response(product_insight: ProductInsights) -> ProductInsightResponse:
    response = ProductInsightResponse(**product_insight.__dict__)

    return response