"""
Custom exception classes for the application.
"""

from fastapi import HTTPException, status


class ObsidianSyncException(Exception):
    """Base exception class for Obsidian Sync API."""
    pass


class PostNotFoundError(ObsidianSyncException):
    """Raised when a post is not found."""
    pass


class InvalidAttachmentPathError(ObsidianSyncException):
    """Raised when attachment path format is invalid."""
    pass


class MissingRequiredFieldError(ObsidianSyncException):
    """Raised when required frontmatter field is missing."""
    pass


class FileOperationError(ObsidianSyncException):
    """Raised when file operation fails."""
    pass


# HTTP Exception factories
def post_not_found_http_exception(post_id: str) -> HTTPException:
    """Create HTTP exception for post not found."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No article found for postId: {post_id}"
    )


def invalid_attachment_path_http_exception(path: str) -> HTTPException:
    """Create HTTP exception for invalid attachment path."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Attachment path invalid: {path}. Must be media/{{ext}}/{{postId}}/{{postId}}-{{13digit}}.{{ext}} (全部小寫)"
    )


def missing_required_field_http_exception(field: str) -> HTTPException:
    """Create HTTP exception for missing required field."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Missing required frontmatter field: {field}"
    ) 