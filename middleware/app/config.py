import os
from dotenv import load_dotenv

load_dotenv()

# Legacy Django API URL
LEGACY_API_URL = os.getenv("LEGACY_API_URL", "http://127.0.0.1:8000/api")

# API key for middleware authentication
API_KEY = os.getenv("API_KEY", "dev-api-key-change-in-production")

# App settings
APP_VERSION ="1.0.0"
APP_TITLE =""