"""
Post schemas for API validation.
"""

from pydantic import BaseModel, Field
from typing import Any, List, Optional
from .attachment import AttachmentSchema


class PostRequestSchema(BaseModel):
    """Schema for post upsert request."""
    # Only truly essential fields are required
    title: str = Field(..., description="Post title")
    date: str = Field(..., description="Post date in ISO format")
    
    # Content and metadata with defaults
    content: str = Field("", description="Post content in Markdown")
    author: str = Field("Anonymous", description="Post author")
    description: Optional[str] = Field(None, description="Post description")
    categories: Optional[str] = Field(None, description="Post categories")
    tags: Optional[List[str]] = Field(None, description="Post tags")
    postId: Optional[str] = Field(None, description="Post ID (empty for new posts)")
    
    # Hugo frontmatter options with sensible defaults (all optional)
    draft: bool = Field(False, description="Whether post is draft")
    showToc: bool = Field(True, description="Show table of contents")
    TocOpen: bool = Field(False, description="Table of contents open by default")
    hidemeta: bool = Field(False, description="Hide metadata")
    comments: bool = Field(True, description="Enable comments")
    disableHLJS: bool = Field(False, description="Disable highlight.js")
    disableShare: bool = Field(False, description="Disable share buttons")
    hideSummary: bool = Field(False, description="Hide summary")
    searchHidden: bool = Field(False, description="Hide from search")
    ShowReadingTime: bool = Field(True, description="Show reading time")
    ShowBreadCrumbs: bool = Field(True, description="Show breadcrumbs")
    ShowPostNavLinks: bool = Field(True, description="Show post navigation links")
    ShowWordCount: bool = Field(True, description="Show word count")
    ShowRssButtonInSectionTermList: bool = Field(False, description="Show RSS button in section term list")
    UseHugoToc: bool = Field(True, description="Use Hugo table of contents")
    
    # Attachments
    attachments: List[AttachmentSchema] = Field([], description="Post attachments")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My Example Post",
                "date": "2024-01-01T00:00:00+08:00",
                "content": "# Hello World\n\nThis is my first post!",
                "categories": "Blog",
                "tags": ["example", "tutorial"],
                "author": "Author Name"
            }
        } 