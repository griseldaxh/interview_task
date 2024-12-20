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
import config
app = FastAPI(title="Amazon Product Intelligence")

conn = psycopg2.connect(
    dbname=config.POSTGRES_DB,
    user=config.POSTGRES_USERNAME,
    password=config.POSTGRES_PASSWORD,
    host="localhost",  # or your PostgreSQL host
    port="5432"        # Default PostgreSQL port
)

products_repository = ProductsRepository(conn = conn)

@app.get("/api/v1/products/{product_id}/insights")
async def get_product_insights(product_id: str):
    """
    Get insights for a specific product
    """
    # TODO: Implement insight retrieval
    pass

@app.get("/api/v1/products", response_model = list[ProductSummary])
async def get_products(page: int = 1, page_size: int = 50):
    print("hello")
    """
    Get all products with pagination
    """
    products = products_repository.get_products_summary(page, page_size)
    jsonified_objects = map_to_response(products)
    
    return jsonified_objects