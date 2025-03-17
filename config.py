import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")