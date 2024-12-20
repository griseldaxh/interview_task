from models.product_summary_entity import ProductSummaryEntity
from models.products_controller_schema import ProductSummary
def map_to_response(product_summaries: list[ProductSummaryEntity]) -> list[ProductSummary]:

    response = []

    for product_summary in product_summaries:
        response_product_summary = ProductSummary(**product_summary.__dict__)
        response.append(response_product_summary)
    return response