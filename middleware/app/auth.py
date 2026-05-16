from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from .config import API_KEY

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Validates the API key from the request header.
    In production, this would check against a database of valid keys
    with associated permissions and rate limits.
    """
    if api_key is None:
        # No key at all - 401 Unautohorized
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Include X-API-Key header"
        )
    if api_key != API_KEY:
        # Wrong key - 403 Firbidden ("your ID is fake")
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    
    return api_key