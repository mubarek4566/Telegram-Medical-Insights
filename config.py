from dotenv import load_dotenv
import os

# Load variables from .env into the environment
load_dotenv()

# Telegram credentials
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER")

# Database credentials
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

# YOLO model path
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH")

# FastAPI settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Optional: Raise an error if critical vars are missing
required_vars = [TELEGRAM_API_ID, TELEGRAM_API_HASH, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]
if not all(required_vars):
    raise EnvironmentError("Missing one or more critical environment variables.")
