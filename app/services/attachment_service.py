"""
Attachment processing service.
"""

import re
from typing import List, Dict, Tuple
from pathlib import Path
from loguru import logger

from ..models.attachment import Attachment
from ..config import settings
from ..utils.file_utils import decode_base64_and_write, delete_directory
from ..utils.validation import validate_attachment_path_format, extract_attachment_path_components
from ..exceptions import InvalidAttachmentPathError


class AttachmentService:
    """Service for handling attachment operations."""
    
    def __init__(self):
        self.static_root = settings.static_root
    
    def validate_attachments(self, attachments: List[Dict[str, str]]) -> List[Tuple[str, str]]:
        """
        Validate attachments and return list of (path, data) tuples.
        """
        validated_attachments = []
        
        for att in attachments:
            att_path = att.get("path")
            att_data = att.get("data")
            att_name = att.get("name")
            
            if not att_path or not att_data or not att_name:
                continue
                
            # Validate path format
            if not validate_attachment_path_format(att_path):
                logger.error(f"[validate_attachments] Invalid attachment path format: {att_path}")
                raise InvalidAttachmentPathError(att_path)
            
            # Extract components and generate normalized path
            components = extract_attachment_path_components(att_path)
            timestamp = components["timestamp"]
            ext = components["ext"]
            file_ext = components["file_ext"]
            
            validated_attachments.append((att_path.lower(), att_data))
        
        return validated_attachments
    
    def create_attachment_mapping(self, attachments: List[Dict[str, str]], post_id: str) -> Dict[str, str]:
        """
        Create mapping from attachment name to blog URL path.
        """
        attachment_map = {}
        
        for att in attachments:
            att_path = att.get("path", "")
            att_name = att.get("name", "")
            
            if not att_path or not att_name:
                continue
                
            try:
                components = extract_attachment_path_components(att_path)
                logger.debug(f"[create_attachment_mapping] Components: {components}")
                ext = components["ext"]
                timestamp = components["timestamp"]
                file_ext = components["file_ext"]
                
                blog_path = f"/blog/media/{ext}/{post_id}/{post_id}-{timestamp}.{file_ext}"
                attachment_map[att_name] = blog_path
            except Exception as e:
                logger.warning(f"Failed to process attachment {att_name}: {e}")
                continue
        
        return attachment_map
    
    def save_attachments(self, validated_attachments: List[Tuple[str, str]], post_id: str) -> None:
        """
        Save validated attachments to static directory.
        """
        for att_path, att_data in validated_attachments:
            try:
                components = extract_attachment_path_components(att_path)
                ext = components["ext"]
                timestamp = components["timestamp"]
                file_ext = components["file_ext"]
                
                # Generate actual storage path
                storage_path = f"media/{ext}/{post_id}/{post_id}-{timestamp}.{file_ext}"
                full_path = self.static_root / storage_path
                
                decode_base64_and_write(full_path, att_data)
                
            except Exception as e:
                logger.error(f"Failed to save attachment {att_path}: {e}")
    
    def delete_attachments(self, post_id: str) -> None:
        """
        Delete all attachments for a post.
        """
        media_dir = self.static_root / "media"
        if not media_dir.exists():
            return
            
        for ext_dir in media_dir.iterdir():
            if ext_dir.is_dir():
                post_dir = ext_dir / post_id
                if post_dir.exists() and post_dir.is_dir():
                    delete_directory(post_dir)
    
    def process_obsidian_image_syntax(self, content: str, attachment_map: Dict[str, str]) -> str:
        """
        Replace Obsidian image syntax with markdown image syntax.
        """
        def replace_obsidian_img(match):
            fname = match.group(1)
            path = attachment_map.get(fname)
            if path:
                return f"![]({path})"
            else:
                return match.group(0)
        
        return re.sub(r"!\[\[([^\]]+)\]\]", replace_obsidian_img, content) 