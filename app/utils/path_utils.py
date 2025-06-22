"""
Path utility functions.
"""

from pathlib import Path
from typing import Union, Optional


def get_category_directory_name(categories: Union[str, list]) -> str:
    """Get category directory name from categories field."""
    if isinstance(categories, list) and categories:
        return categories[0].lower().replace(" ", "_")
    elif isinstance(categories, str) and categories.strip():
        return categories.lower().replace(" ", "_")
    return "uncategorized"


def generate_content_path(content_root: Path, category_dir: str, filename: str) -> Path:
    """Generate full path for content file."""
    return content_root / category_dir / filename


def generate_static_path(static_root: Path, relative_path: str) -> Path:
    """Generate full path for static file."""
    return static_root / relative_path


def find_post_in_categories(content_root: Path, post_id: str) -> Path:
    """Find post file across all category directories."""
    for category_dir in content_root.iterdir():
        if category_dir.is_dir():
            md_path = category_dir / f"{post_id}.md"
            if md_path.exists():
                return md_path
    raise FileNotFoundError(f"Post {post_id} not found in any category directory")


def get_category_from_path(file_path: Path, content_root: Path) -> Optional[str]:
    """Extract category directory name from file path."""
    try:
        # Get relative path from content root
        relative_path = file_path.relative_to(content_root)
        # Get the first directory (category)
        if relative_path.parts:
            return relative_path.parts[0]
        return None
    except ValueError:
        # Path is not relative to content_root
        return None


def compare_category_paths(current_path: Path, new_categories: Union[str, list], content_root: Path) -> bool:
    """
    Compare if current post path matches new categories.
    Returns True if they are different (need to move), False if same.
    """
    current_category = get_category_from_path(current_path, content_root)
    new_category = get_category_directory_name(new_categories)
    
    return current_category != new_category 