"""
Response schemas for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PostUpsertResponse(BaseModel):
    """Response schema for post upsert operation."""
    postId: str = Field(..., description="Post ID")
    status: str = Field(..., description="Operation status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "postId": "12345678-1234-1234-1234-123456789012",
                "status": "success"
            }
        }


class PostDeleteResponse(BaseModel):
    """Response schema for post delete operation."""
    deleted: bool = Field(..., description="Whether deletion was successful")
    postId: str = Field(..., description="Post ID")
    status: str = Field(..., description="Operation status")
    message: Optional[str] = Field(None, description="Additional message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "deleted": True,
                "postId": "12345678-1234-1234-1234-123456789012",
                "status": "success"
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    status: str = Field("error", description="Status indicator")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Invalid request",
                "detail": "Missing required field: title"
            }
        } 