"""
Experiment-related API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from neuromosaic.api.dependencies import get_db, get_orchestrator, get_db_orchestrator
from neuromosaic.api.schemas import Experiment, ExperimentCreate
from neuromosaic.results_db.interface import IResultsDB
from neuromosaic.orchestrator.interface import IOrchestrator

router = APIRouter()


@router.get("/", response_model=List[Experiment])
async def list_experiments(
    skip: int = Query(0, description="Number of experiments to skip"),
    limit: int = Query(100, description="Maximum number of experiments to return"),
    db: IResultsDB = Depends(get_db),
) -> List[Experiment]:
    """
    List all experiments with pagination.

    Args:
        skip: Number of experiments to skip
        limit: Maximum number of experiments to return
        db: Database instance from dependency

    Returns:
        List[Experiment]: List of experiments
    """
    experiments = db.list_experiments(skip=skip, limit=limit)
    return experiments


@router.get("/{experiment_id}", response_model=Experiment)
async def get_experiment(
    experiment_id: str,
    db: IResultsDB = Depends(get_db),
) -> Experiment:
    """
    Get a specific experiment by ID.

    Args:
        experiment_id: Unique experiment identifier
        db: Database instance from dependency

    Returns:
        Experiment: Experiment details

    Raises:
        HTTPException: If experiment is not found
    """
    experiment = db.get_experiment(experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@router.post("/run", response_model=Experiment)
async def run_experiment(
    experiment: ExperimentCreate,
    db_orchestrator: tuple[IResultsDB, IOrchestrator] = Depends(get_db_orchestrator),
) -> Experiment:
    """
    Start a new experiment run.

    Args:
        experiment: Experiment configuration
        db_orchestrator: Tuple of database and orchestrator instances

    Returns:
        Experiment: Created experiment details
    """
    db, orchestrator = db_orchestrator

    # Create experiment in database
    experiment_id = db.create_experiment(
        name=experiment.name,
        description=experiment.description,
        config=experiment.config,
    )

    # Start experiment run
    orchestrator.schedule_experiment(experiment_id)

    # Return created experiment
    return db.get_experiment(experiment_id)


@router.delete("/{experiment_id}")
async def delete_experiment(
    experiment_id: str,
    db_orchestrator: tuple[IResultsDB, IOrchestrator] = Depends(get_db_orchestrator),
) -> dict:
    """
    Delete an experiment.

    Args:
        experiment_id: Unique experiment identifier
        db_orchestrator: Tuple of database and orchestrator instances

    Returns:
        dict: Success message

    Raises:
        HTTPException: If experiment is not found or cannot be deleted
    """
    db, orchestrator = db_orchestrator

    # Check if experiment exists
    if db.get_experiment(experiment_id) is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Stop experiment if running
    orchestrator.stop_experiment(experiment_id)

    # Delete from database
    db.delete_experiment(experiment_id)

    return {"message": "Experiment deleted successfully"}
