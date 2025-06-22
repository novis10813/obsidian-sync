"""
File operations service.
"""

from pathlib import Path
from typing import Optional, Union
from loguru import logger

from ..config import settings
from ..utils.file_utils import write_text_file, delete_file, generate_frontmatter
from ..utils.path_utils import (
    generate_content_path, 
    get_category_directory_name, 
    find_post_in_categories,
    get_category_from_path,
    compare_category_paths
)
from ..exceptions import PostNotFoundError, FileOperationError


class FileService:
    """Service for file system operations."""
    
    def __init__(self):
        self.content_root = settings.content_root
    
    def post_exists(self, post_id: str) -> bool:
        """Check if a post exists in any category directory."""
        try:
            find_post_in_categories(self.content_root, post_id)
            return True
        except FileNotFoundError:
            return False
    
    def get_post_path(self, post_id: str) -> Optional[Path]:
        """Get the path of an existing post."""
        try:
            return find_post_in_categories(self.content_root, post_id)
        except FileNotFoundError:
            return None
    
    def get_post_category(self, post_id: str) -> Optional[str]:
        """Get the current category of an existing post."""
        post_path = self.get_post_path(post_id)
        if post_path:
            return get_category_from_path(post_path, self.content_root)
        return None
    
    def should_move_post(self, current_path: Path, new_categories: Union[str, list]) -> bool:
        """Check if post should be moved to a different category directory."""
        if not current_path or not current_path.exists():
            return False
        
        return compare_category_paths(current_path, new_categories, self.content_root)
    
    def move_post_to_new_category(self, post_id: str, current_path: Path, new_categories: Union[str, list]) -> Path:
        """
        Safely move post from current path to new category directory.
        Returns the new path after successful move.
        """
        logger.info(f"[move] Moving post {post_id} to new category")
        
        # Generate new path
        new_category_dir = get_category_directory_name(new_categories)
        filename = f"{post_id}.md"
        new_path = generate_content_path(self.content_root, new_category_dir, filename)
        
        try:
            # Ensure target directory exists
            new_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read current file content
            current_content = current_path.read_text(encoding='utf-8')
            
            # Write to new location
            write_text_file(new_path, current_content)
            
            # Delete old file after successful write
            if new_path.exists():
                delete_file(current_path)
                logger.info(f"[move] Successfully moved post {post_id} from {current_path} to {new_path}")
                return new_path
            else:
                raise FileOperationError(f"Failed to create new file at {new_path}")
                
        except Exception as e:
            logger.error(f"[move] Failed to move post {post_id}: {str(e)}")
            raise FileOperationError(f"Failed to move post {post_id}: {str(e)}")
    
    def save_post_content(self, post_id: str, frontmatter_data: dict, content: str, categories: str) -> Path:
        """Save post content to appropriate category directory."""
        category_dir = get_category_directory_name(categories)
        filename = f"{post_id}.md"
        
        # Generate markdown content
        frontmatter = generate_frontmatter(frontmatter_data)
        md_content = frontmatter + content
        
        # Generate file path and save
        file_path = generate_content_path(self.content_root, category_dir, filename)
        write_text_file(file_path, md_content)
        
        return file_path
    
    def delete_post(self, post_id: str) -> bool:
        """Delete a post file."""
        post_path = self.get_post_path(post_id)
        if post_path:
            return delete_file(post_path)
        return False 