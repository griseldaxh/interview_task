import os

POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")