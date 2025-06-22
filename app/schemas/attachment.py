"""
Attachment schemas for API validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class AttachmentSchema(BaseModel):
    """Schema for attachment data validation."""
    name: str = Field(..., description="Attachment filename")
    path: str = Field(..., description="Attachment path in media/ext/postId/postId-timestamp.ext format")
    data: str = Field(..., description="Base64 encoded file data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "example.webp",
                "path": "media/webp/my-post/my-post-1234567890123.webp",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            }
        } 