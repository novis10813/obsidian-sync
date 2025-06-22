"""
File utility functions.
"""

import base64
import shutil
from pathlib import Path
from typing import Dict, Any
from loguru import logger
from ..exceptions import FileOperationError


def ensure_directory_exists(path: Path) -> None:
    """Ensure directory exists, create if not."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise FileOperationError(f"Failed to create directory {path}: {e}")


def write_text_file(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write text content to file."""
    try:
        ensure_directory_exists(file_path.parent)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        logger.info(f"Wrote text file: {file_path}")
    except Exception as e:
        raise FileOperationError(f"Failed to write text file {file_path}: {e}")


def write_binary_file(file_path: Path, data: bytes) -> None:
    """Write binary data to file."""
    try:
        ensure_directory_exists(file_path.parent)
        with open(file_path, "wb") as f:
            f.write(data)
        logger.info(f"Wrote binary file: {file_path}")
    except Exception as e:
        raise FileOperationError(f"Failed to write binary file {file_path}: {e}")


def decode_base64_and_write(file_path: Path, base64_data: str) -> None:
    """Decode base64 data and write to file."""
    try:
        decoded_data = base64.b64decode(base64_data)
        write_binary_file(file_path, decoded_data)
    except Exception as e:
        raise FileOperationError(f"Failed to decode and write base64 data to {file_path}: {e}")


def delete_file(file_path: Path) -> bool:
    """Delete a file if it exists."""
    try:
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {e}")
        return False


def delete_directory(dir_path: Path) -> bool:
    """Delete a directory and its contents if it exists."""
    try:
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)
            logger.info(f"Deleted directory: {dir_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete directory {dir_path}: {e}")
        return False


def generate_frontmatter(data: Dict[str, Any]) -> str:
    """Generate frontmatter string from data dictionary."""
    frontmatter = ["---"]
    for k, v in data.items():
        if k not in ("content", "attachments", "filename"):
            value = v if v is not None else ""
            frontmatter.append(f"{k}: {value}")
    frontmatter.append("---\n")
    return "\n".join(frontmatter) 