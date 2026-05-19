from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from ..schemas import (
    DocumentCreate, DocumentResponse, DocumentDetail,
    StatusTransition, StatsResponse
)
from ..services import legacy_api
from ..auth import verify_api_key

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search title or content"),
    category: Optional[int] = Query(None, description="Filter by category ID"),
    page: int = Query(1, ge=1, description="Page number"),
    api_key: str = Depends(verify_api_key),
):
    """List documents with optional filtering and pagination."""
    try:
        data = await legacy_api.get_documents(
            status=status, search=search, category=category, page=page
        )
        # Handle paginated response from Django
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Legacy API error: {str(e)}")


@router.get("/stats", response_model=StatsResponse)
async def get_stats(api_key: str = Depends(verify_api_key)):
    """Get document publishing statistics."""
    try:
        return await legacy_api.get_document_stats()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Legacy API error: {str(e)}")


@router.get("/{document_id}", response_model=DocumentDetail)
async def get_document(document_id: int, api_key: str = Depends(verify_api_key)):
    """Get full document details with status history."""
    try:
        return await legacy_api.get_document(document_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Document not found")


@router.post("/", response_model=DocumentDetail, status_code=201)
async def create_document(doc: DocumentCreate, api_key: str = Depends(verify_api_key)):
    """Create a new document in draft status."""
    try:
        return await legacy_api.create_document(doc.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create document: {str(e)}")


@router.post("/{document_id}/transition", response_model=DocumentDetail)
async def transition_document(
    document_id: int,
    transition: StatusTransition,
    api_key: str = Depends(verify_api_key),
):
    """Transition a document to a new status (with audit logging)."""
    valid = ["draft", "review", "approved", "published", "archived"]
    if transition.status not in valid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {valid}"
        )
    try:
        return await legacy_api.transition_document(
            document_id, transition.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Transition failed: {str(e)}")