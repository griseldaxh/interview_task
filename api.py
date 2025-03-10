from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.products_controller_schema import ProductSummary
import psycopg2
from psycopg2 import sql
from repository.products_repository import ProductsRepository
from repository.products_mapper import map_to_response
from product_insights_service import ProductInsightsService
import config
from openai import OpenAI
from analyzer import ProductAnalyzer
from logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="Amazon Product Intelligence")

conn = psycopg2.connect(
    dbname=config.POSTGRES_DB,
    user=config.POSTGRES_USERNAME,
    password=config.POSTGRES_PASSWORD,
    host="localhost",  # or your PostgreSQL host
    port="5432"        # Default PostgreSQL port
)
client = OpenAI(api_key=config.OPEN_API_KEY)

products_repository = ProductsRepository(conn = conn)
product_analyzer = ProductAnalyzer(llm_client=client)
product_insights_service = ProductInsightsService(products_repository=products_repository,
                                                  product_analyzer=product_analyzer)


@app.get("/api/v1/products/{product_id}/insights")
async def get_product_insights(product_id: str):
    product_id = product_id.strip()
    logger.info(f"Received request to analyze {product_id}")
    """
    Get insights for a specific product
    """
    insight = await product_insights_service.get_insight(product_id)
    
    print(insight)
    return insight

# TODO can delete; test endpoint for retrieving product reviews
# @app.get("/api/v1/products/{product_id}/reviews")
# async def get_product_insights(product_id: str):
#     """
#     Get insights for a specific product
#     """
#     products = products_repository.get_product_reviews(product_id)
#     jsonified_objects = map_to_response(products)
    
#     return jsonified_objects

@app.get("/api/v1/products", response_model = list[ProductSummary])
async def get_products(page: int = 1, page_size: int = 50):
    print("hello")
    """
    Get all products with pagination
    """
    products = products_repository.get_products_summary(page, page_size)
    jsonified_objects = map_to_response(products)
    
    return jsonified_objects