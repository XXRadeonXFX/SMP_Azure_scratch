"""
Group Manager Service - Main Application
Sprint 1, Step 1: Basic FastAPI setup with health check
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.api.v1 import health, azure_test

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting Group Manager Service")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Service running on port: {settings.PORT}")
    yield
    # Shutdown
    logger.info("Shutting down Group Manager Service")


# Initialize FastAPI app
app = FastAPI(
    title="Group Manager Service",
    description="Azure AD Group Management Service - Python Port",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(azure_test.router, tags=["Azure"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Group Manager Service",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
