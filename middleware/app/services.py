import httpx
from .config import LEGACY_API_URL
import logging

logger = logging.getLogger("middleware.services")

class LegacyAPIService:
    """Service layer that comunicates with legacy Dango REST API"""

    def __init__(self):
        self.base_url = LEGACY_API_URL

    async def _get(self, path: str, params: dict =None) -> dict:
        async with httpx.AsyncClient() as client: # Creates a temporary HTTP client, auto-closes when done
            url = f"{self.base_url}/{path}"
            logger.info(f"GET {url} params={params}")
            response = await client.get(url, params=params, timeout=10.0) # await = wait without blocking
            response.raise_for_status() #Throws an error if status code is 4xx or 5xx
            return response.json() # Parse JSON response into a Python dict
    
    async def _post(self, path: str, data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{path}"
            logger.info(f"POST {url}")
            response = await client.post(url, json=data, timeout=10.0)  # json= auto-serializes dict to JSON
            response.raise_for_status() #Throws an error if status code is 4xx or 5xx
            return response.json()
            