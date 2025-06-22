"""
Validation utility functions.
"""

import re
from typing import List, Dict, Any
from ..exceptions import MissingRequiredFieldError, InvalidAttachmentPathError


def validate_required_frontmatter_fields(data: Dict[str, Any]) -> None:
    """Validate that all required frontmatter fields are present."""
    required_fields = [
        "title", "description", "date", "tags", "categories", "author", "draft", 
        "showToc", "TocOpen", "hidemeta", "comments", "disableHLJS", "disableShare", 
        "hideSummary", "searchHidden", "ShowReadingTime", "ShowBreadCrumbs", 
        "ShowPostNavLinks", "ShowWordCount", "ShowRssButtonInSectionTermList", "UseHugoToc"
    ]
    
    for field in required_fields:
        if field not in data:
            raise MissingRequiredFieldError(f"Missing required frontmatter field: {field}")


def validate_attachment_path_format(path: str) -> bool:
    """Validate attachment path format."""
    pattern = r"media/([a-z0-9]+)/([\w\-_]+)/([\w\-_]+)-(\d{13})\.([a-z0-9]+)"
    return bool(re.match(pattern, path.lower()))


def extract_attachment_path_components(path: str) -> Dict[str, str]:
    """Extract components from attachment path."""
    pattern = r"media/([a-z0-9]+)/([\w\-_]+)/([\w\-_]+)-(\d{13})\.([a-z0-9]+)"
    match = re.match(pattern, path.lower())
    if not match:
        raise InvalidAttachmentPathError(f"Invalid attachment path format: {path}")
    
    return {
        "ext": match.group(1),
        "post_id": match.group(2),
        "timestamp": match.group(4),
        "file_ext": match.group(5)
    } 