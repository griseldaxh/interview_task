# Define main herefrom fastapi import FastAPI
from app.api import app
from dotenv import load_dotenv
import os

load_dotenv()

# Access the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)