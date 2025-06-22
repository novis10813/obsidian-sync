"""
Post processing service.
"""

import uuid
from typing import Dict, Any
from loguru import logger

from ..schemas.post import PostRequestSchema
from ..schemas.responses import PostUpsertResponse, PostDeleteResponse
from ..exceptions import PostNotFoundError, post_not_found_http_exception
from .file_service import FileService
from .attachment_service import AttachmentService


class PostService:
    """Service for post processing operations."""
    
    def __init__(self):
        self.file_service = FileService()
        self.attachment_service = AttachmentService()
    
    def upsert_post(self, post_data: PostRequestSchema) -> PostUpsertResponse:
        """
        Create or update a post.
        """
        logger.info(f"[upsert] Processing post: {post_data.title}")
        
        # Determine if this is a new post or update
        post_id = post_data.postId
        is_new = not post_id or not str(post_id).strip()
        
        if is_new:
            # Generate new post ID
            post_id = str(uuid.uuid4())
            logger.info(f"[upsert] Creating new post with ID: {post_id}")
        else:
            # Validate existing post
            if not self.file_service.post_exists(post_id):
                raise post_not_found_http_exception(post_id)
            logger.info(f"[upsert] Updating existing post: {post_id}")
            
            # Check if post needs to be moved to different category
            current_path = self.file_service.get_post_path(post_id)
            new_categories = post_data.categories
            
            if current_path and self.file_service.should_move_post(current_path, new_categories):
                logger.info(f"[upsert] Post {post_id} needs category migration")
                try:
                    # Move post to new category directory
                    new_path = self.file_service.move_post_to_new_category(
                        post_id, current_path, new_categories
                    )
                    logger.info(f"[upsert] Post {post_id} successfully moved to new category")
                except Exception as e:
                    logger.error(f"[upsert] Failed to move post {post_id}: {str(e)}")
                    # Continue with update even if move fails
        
        # Convert request data to dict for processing
        data_dict = post_data.dict()
        data_dict["postId"] = post_id
        
        # Process attachments
        logger.debug("[upsert] Processing attachments")
        attachments = data_dict.get("attachments", [])
        validated_attachments = self.attachment_service.validate_attachments(attachments)
        logger.debug("[upsert] Validated attachments successfully")
        attachment_map = self.attachment_service.create_attachment_mapping(attachments, post_id)
        logger.debug("[upsert] Attachment map successfully created")
        
        # Process content with image syntax conversion
        logger.debug("[upsert] Processing content")
        content = data_dict.get("content", "")
        processed_content = self.attachment_service.process_obsidian_image_syntax(content, attachment_map)
        
        # Save post content
        logger.debug("[upsert] Saving post content")
        self.file_service.save_post_content(
            post_id=post_id,
            frontmatter_data=data_dict,
            content=processed_content,
            categories=data_dict.get("categories", "")
        )
        
        # Save attachments
        logger.debug("[upsert] Saving attachments")
        self.attachment_service.save_attachments(validated_attachments, post_id)
        
        logger.info(f"[upsert] Successfully processed post: {post_id}")
        return PostUpsertResponse(postId=post_id, status="success")
    
    def delete_post(self, post_id: str) -> PostDeleteResponse:
        """
        Delete a post and its attachments.
        """
        logger.info(f"[delete] Deleting post: {post_id}")
        
        # Delete post file
        post_deleted = self.file_service.delete_post(post_id)
        
        # Delete attachments
        self.attachment_service.delete_attachments(post_id)
        
        if not post_deleted:
            return PostDeleteResponse(
                deleted=False,
                postId=post_id,
                status="not_found",
                message="Post not found"
            )
        
        logger.info(f"[delete] Successfully deleted post: {post_id}")
        return PostDeleteResponse(
            deleted=True,
            postId=post_id,
            status="success"
        ) 