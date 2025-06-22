"""
Health check endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str


@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="Obsidian Sync API",
        version="0.1.0"
    ) 