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
    
    # Documents
    async def get_documents(self, status: str = None, search: str = None, category: int = None, page: int =1) -> dict:
        params = {"page":page}
        if status:
            params["status"] = status
        if search:
            params["search"] = search
        if category:
            params["category"] = category
        return await self._get("documents/", params)
    
    async def get_document(self, doc_id: int) -> dict:
        return await self._get(f"documents/{doc_id}/")
    
    async def create_document(self, data: dict) -> dict:
        return await self._post("documents/", data)
    
    async def transition_document(self, doc_id: int, data: dict) -> dict:
        return await self._post(f"documents/{doc_id}/transition/", data)

    async def get_document_stats(self) -> dict:
        return await self._get("documents/stats/")

    # --- Categories ---
    async def get_categories(self) -> dict:
        return await self._get("categories/")

    async def get_category(self, cat_id: int) -> dict:
        return await self._get(f"categories/{cat_id}/")
    
    # --- Authors ---
    async def get_authors(self, agency: str = None) -> dict:
        params = {}
        if agency:
            params["agency"] = agency
        return await self._get("authors/", params)
    
    # --- Health ---
    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/documents/stats/", timeout = 5.0
                )
                return response.status_code == 200 # 200 alive-> True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

legacy_api = LegacyAPIService()