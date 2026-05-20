import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/classicmodels"
)

ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
MAX_RETRIES = 3
