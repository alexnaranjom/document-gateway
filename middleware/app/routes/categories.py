from fastapi import APIRouter, Depends
from ..schemas import CategoryResponse
from ..services import legacy_api
from ..auth import verify_api_key

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
async def list_categories(api_key: str = Depends(verify_api_key)):
    """List all document categories."""
    data = await legacy_api.get_categories()
    if isinstance(data, dict) and "results" in data:
        return data["results"]
    return data
