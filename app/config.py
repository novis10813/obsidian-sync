"""
Application configuration management.
"""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    title: str = "Obsidian Sync API"
    version: str = "0.1.0"
    description: str = "API for syncing Obsidian notes to Hugo static site"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 1312
    reload: bool = True
    
    # Path Settings
    content_root: Path = Path("/app/content")
    static_root: Path = Path("/app/static")
    
    # Logging
    log_level: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        env_prefix = "OBSIDIAN_SYNC_"
        extra = "ignore"  # 忽略額外的環境變數


# Global settings instance
settings = Settings() 