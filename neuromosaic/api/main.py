"""
Main FastAPI application entry point.

The main entry point for the Neuromosaic FastAPI backend. It defines the 
FastAPI application, configures middleware, and includes endpoint routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from neuromosaic.api.config import get_api_settings
from neuromosaic.api.dependencies import on_startup, on_shutdown
from neuromosaic.api.endpoints import experiments, architectures, metrics, export

# Create FastAPI app instance
app = FastAPI(
    title="Neuromosaic API",
    description="Backend service for experiment management, architecture exploration, and metrics retrieval",
    version="0.1.0",
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
)

# Configure CORS
settings = get_api_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from each endpoint file
app.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
app.include_router(
    architectures.router, prefix="/architectures", tags=["architectures"]
)
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(export.router, prefix="/export", tags=["export"])


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {
        "message": "Welcome to Neuromosaic API",
        "status": "running",
        "version": "0.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


def run_server():
    """Run the FastAPI server using uvicorn."""
    uvicorn.run(
        "neuromosaic.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
        reload=settings.reload,
    )


if __name__ == "__main__":
    run_server()
