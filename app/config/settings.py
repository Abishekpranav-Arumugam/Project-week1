import os

from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "product_app")
DB_PASSWORD = os.getenv("Abishek@2004")
DB_NAME = os.getenv("DB_NAME", "product_db")


if not DB_PASSWORD:
    raise RuntimeError(
        "DB_PASSWORD is not configured in the .env file."
    )