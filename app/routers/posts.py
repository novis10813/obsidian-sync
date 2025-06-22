"""
Post management endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

from ..schemas.post import PostRequestSchema
from ..schemas.responses import PostUpsertResponse, PostDeleteResponse, ErrorResponse
from ..services.post_service import PostService
from ..exceptions import (
    ObsidianSyncException,
    InvalidAttachmentPathError,
    MissingRequiredFieldError,
    invalid_attachment_path_http_exception,
    missing_required_field_http_exception
)

router = APIRouter(
    prefix="/api",
    tags=["Posts"]
)

# Initialize service
post_service = PostService()


@router.post("/posts", response_model=PostUpsertResponse)
async def upsert_post(post_data: PostRequestSchema):
    """
    Create or update a post.
    
    - **postId**: Leave empty for new posts, provide existing ID for updates
    - **title**: Post title (required)
    - **description**: Post description (required)
    - **content**: Post content in Markdown format
    - **attachments**: List of attachments with base64 encoded data
    """
    try:
        return post_service.upsert_post(post_data)
    except InvalidAttachmentPathError as e:
        raise invalid_attachment_path_http_exception(str(e))
    except MissingRequiredFieldError as e:
        raise missing_required_field_http_exception(str(e))
    except ObsidianSyncException as e:
        logger.error(f"Post upsert error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in post upsert: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/posts/{post_id}", response_model=PostDeleteResponse)
async def delete_post(post_id: str):
    """
    Delete a post and its associated attachments.
    
    - **post_id**: The ID of the post to delete
    """
    try:
        result = post_service.delete_post(post_id)
        
        if not result.deleted:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=result.dict()
            )
        
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in post deletion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 