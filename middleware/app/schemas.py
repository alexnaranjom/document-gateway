from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

# Category schemas
class CategoryBase(BaseModel):
    name: str
    code: str
    description: str = ""

class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)  # Pydantic V2 style (replaces class Config)

    id:int
    document_count: Optional[int] = 0

class AuthorBase(BaseModel):
    name : str
    agency : str
    email: EmailStr  # EmailStr validates that the string is a valid email format

class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id:int

class DocumentCreate(BaseModel):
    """what the CLIENT SENDS (slim — just IDs, not full objects)"""
    title : str
    document_number : str
    category_id : int
    author_id : int
    content_summary : str = ""
    page_count : int = 0

class DocumentResponse(BaseModel):
    """what the API RETURNS in LIST views (lightweight, flattened names)"""
    model_config = ConfigDict(from_attributes=True)

    id:int
    title: str
    category_name: Optional[str] = None  # Just the ID — client sends 1, not the full category object
    author_name: Optional[str] = None
    status: str
    page_count: int
    submitted_date: Optional[datetime] = None
    published_date: Optional[datetime] = None

class DocumentDetail(BaseModel):
    """what the API RETURNS for a SINGLE document (full nested objects + history)"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    document_number: str
    category: Optional[CategoryResponse] = None  # Full nested object
    author: Optional[AuthorResponse] = None
    status: str
    content_summary: str
    page_count: int
    submitted_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status_history: list = []

# --- Stats ---
# Output for the /stats endpoint
class StatsResponse(BaseModel):
    total_documents: int
    by_status: dict
    categories: int
    authors: int


class StatusTransition(BaseModel):
    """ Input schema for changing a document's status"""
    status: str     # "draft", "review", "approved", etc.
    changed_by: str = "middleware"
    notes: str =""

class HealthResponse(BaseModel):
    status: str
    legacy_backend: str
    version: str
    timestamp: datetime





