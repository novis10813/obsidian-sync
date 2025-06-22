"""
Attachment data models.
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Attachment:
    """Attachment data model."""
    name: str
    path: str
    data: str  # base64 encoded
    
    @property
    def normalized_path(self) -> str:
        """Get normalized (lowercase) path."""
        return self.path.lower()
    
    def validate_path_format(self) -> bool:
        """Validate attachment path format."""
        pattern = r"media/([a-z0-9]+)/([\w\-_]+)/([\w\-_]+)-(\d{13})\.([a-z0-9]+)"
        return bool(re.match(pattern, self.normalized_path))
    
    def extract_path_components(self) -> Optional[dict]:
        """Extract components from attachment path."""
        pattern = r"media/([a-z0-9]+)/([\w\-_]+)/([\w\-_]+)-(\d{13})\.([a-z0-9]+)"
        match = re.match(pattern, self.normalized_path)
        if match:
            return {
                "ext": match.group(1),
                "post_id": match.group(2),
                "timestamp": match.group(4),
                "file_ext": match.group(5)
            }
        return None
    
    def generate_static_path(self, post_id: str) -> str:
        """Generate static file path for storage."""
        components = self.extract_path_components()
        if components:
            ext = components["ext"]
            timestamp = components["timestamp"]
            return f"media/{ext}/{post_id}/{post_id}-{timestamp}.{components['file_ext']}"
        return self.normalized_path
    
    def generate_blog_path(self, post_id: str) -> str:
        """Generate blog URL path for markdown content."""
        components = self.extract_path_components()
        if components:
            ext = components["ext"]
            timestamp = components["timestamp"]
            return f"/blog/media/{ext}/{post_id}/{post_id}-{timestamp}.{components['file_ext']}"
        return f"/blog/{self.normalized_path}" 