"""
Post data models.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from pathlib import Path


@dataclass
class PostMetadata:
    """Post metadata/frontmatter."""
    title: str
    description: str
    date: str
    tags: List[str]
    categories: str
    author: str
    draft: bool
    showToc: bool
    TocOpen: bool
    hidemeta: bool
    comments: bool
    disableHLJS: bool
    disableShare: bool
    hideSummary: bool
    searchHidden: bool
    ShowReadingTime: bool
    ShowBreadCrumbs: bool
    ShowPostNavLinks: bool
    ShowWordCount: bool
    ShowRssButtonInSectionTermList: bool
    UseHugoToc: bool
    postId: Optional[str] = None


@dataclass
class Post:
    """Complete post with metadata and content."""
    metadata: PostMetadata
    content: str
    attachments: List[Dict[str, Any]]
    
    @property
    def post_id(self) -> str:
        """Get post ID."""
        return self.metadata.postId or ""
    
    @property
    def category_dir(self) -> str:
        """Get category directory name."""
        categories = self.metadata.categories
        if isinstance(categories, list) and categories:
            return categories[0].lower().replace(" ", "_")
        elif isinstance(categories, str) and categories.strip():
            return categories.lower().replace(" ", "_")
        return "uncategorized"
    
    @property
    def filename(self) -> str:
        """Get markdown filename."""
        return f"{self.post_id}.md" 