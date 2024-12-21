"""
Architecture-related API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from neuromosaic.api.dependencies import get_db
from neuromosaic.api.schemas import Architecture
from neuromosaic.results_db.interface import IResultsDB

router = APIRouter()


@router.get("/", response_model=List[Architecture])
async def list_architectures(
    skip: int = Query(0, description="Number of architectures to skip"),
    limit: int = Query(100, description="Maximum number of architectures to return"),
    db: IResultsDB = Depends(get_db),
) -> List[Architecture]:
    """
    List all architectures with pagination.

    Args:
        skip: Number of architectures to skip
        limit: Maximum number of architectures to return
        db: Database instance from dependency

    Returns:
        List[Architecture]: List of architectures
    """
    architectures = db.list_architectures(skip=skip, limit=limit)
    return architectures


@router.get("/{architecture_id}", response_model=Architecture)
async def get_architecture(
    architecture_id: str,
    db: IResultsDB = Depends(get_db),
) -> Architecture:
    """
    Get a specific architecture by ID.

    Args:
        architecture_id: Unique architecture identifier
        db: Database instance from dependency

    Returns:
        Architecture: Architecture details

    Raises:
        HTTPException: If architecture is not found
    """
    architecture = db.get_architecture(architecture_id)
    if architecture is None:
        raise HTTPException(status_code=404, detail="Architecture not found")
    return architecture


@router.get("/{architecture_id}/description", response_model=dict)
async def get_architecture_description(
    architecture_id: str,
    db: IResultsDB = Depends(get_db),
) -> dict:
    """
    Get a human-readable description of an architecture.

    Args:
        architecture_id: Unique architecture identifier
        db: Database instance from dependency

    Returns:
        dict: Architecture description

    Raises:
        HTTPException: If architecture is not found
    """
    architecture = db.get_architecture(architecture_id)
    if architecture is None:
        raise HTTPException(status_code=404, detail="Architecture not found")

    # TODO: Implement architecture description generation
    # This could use meta_learning or llm_code_gen to generate descriptions
    description = {
        "name": architecture.name,
        "description": architecture.description or "No description available",
        "components": {
            "encoder": "Description of encoder architecture...",
            "decoder": "Description of decoder architecture...",
        },
    }

    return description
