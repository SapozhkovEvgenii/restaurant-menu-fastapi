import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

TEST_DB_NAME = os.getenv("TEST_POSTGRES_DB")
TEST_DB_USER = os.getenv("TEST_POSTGRES_USER")
TEST_DB_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_HOST = os.getenv("TEST_POSTGRES_HOST")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
TEST_ASYNC_DATABASE_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_HOST}:5432/{TEST_DB_NAME}"
