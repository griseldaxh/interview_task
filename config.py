import os
from dotenv import load_dotenv
load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
OPEN_API_KEY = os.getenv("OPEN_API_KEY")