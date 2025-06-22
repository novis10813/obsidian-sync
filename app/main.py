"""
Obsidian Sync API - FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn

from .config import settings
from .dependencies import setup_logging
from .routers import posts, health
from .schemas.responses import ErrorResponse


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.title,
        version=settings.version,
        description=settings.description,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(posts.router)
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error",
                "detail": str(exc)
            }
        )
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    ) 