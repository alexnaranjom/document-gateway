from fastapi import APIRouter
from datetime import datetime
from ..schemas import HealthResponse
from ..services import legacy_api
from ..config import APP_VERSION

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """check the middleware and legacy backend connectivity"""
    backend_ok = await legacy_api.health_check()
    return HealthResponse(
        status="healthy" if backend_ok else "degraded",
        legacy_backend="connected" if backend_ok else "unreachable",
        version=APP_VERSION,
        timestamp=datetime.now()
    )
