"""
Metrics-related API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta

from neuromosaic.api.dependencies import get_db
from neuromosaic.api.schemas import MetricResponse
from neuromosaic.results_db.interface import IResultsDB

router = APIRouter()


@router.get("/", response_model=List[MetricResponse])
async def get_metrics(
    experiment_id: Optional[str] = Query(None, description="Filter by experiment ID"),
    start_time: Optional[datetime] = Query(
        None, description="Filter metrics after this time"
    ),
    end_time: Optional[datetime] = Query(
        None, description="Filter metrics before this time"
    ),
    metric_names: Optional[List[str]] = Query(
        None, description="Filter by metric names"
    ),
    db: IResultsDB = Depends(get_db),
) -> List[MetricResponse]:
    """
    Get metrics with optional filtering.

    Args:
        experiment_id: Optional experiment ID to filter by
        start_time: Optional start time for filtering
        end_time: Optional end time for filtering
        metric_names: Optional list of metric names to filter by
        db: Database instance from dependency

    Returns:
        List[MetricResponse]: List of metrics matching the filters
    """
    # Default to last 24 hours if no time range specified
    if start_time is None and end_time is None:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=1)

    metrics = db.get_metrics(
        experiment_id=experiment_id,
        start_time=start_time,
        end_time=end_time,
        metric_names=metric_names,
    )
    return metrics


@router.get("/summary", response_model=dict)
async def get_metrics_summary(
    experiment_id: Optional[str] = Query(None, description="Filter by experiment ID"),
    metric_names: Optional[List[str]] = Query(
        None, description="Filter by metric names"
    ),
    db: IResultsDB = Depends(get_db),
) -> dict:
    """
    Get summary statistics for metrics.

    Args:
        experiment_id: Optional experiment ID to filter by
        metric_names: Optional list of metric names to filter by
        db: Database instance from dependency

    Returns:
        dict: Summary statistics for the metrics
    """
    # Get metrics for summary calculation
    metrics = db.get_metrics(
        experiment_id=experiment_id,
        metric_names=metric_names,
    )

    # Calculate summary statistics
    summary = {}
    for metric in metrics:
        for name, value in metric.metrics.items():
            if name not in summary:
                summary[name] = {
                    "min": float("inf"),
                    "max": float("-inf"),
                    "sum": 0,
                    "count": 0,
                }
            stats = summary[name]
            stats["min"] = min(stats["min"], value)
            stats["max"] = max(stats["max"], value)
            stats["sum"] += value
            stats["count"] += 1

    # Calculate averages
    for name, stats in summary.items():
        if stats["count"] > 0:
            stats["avg"] = stats["sum"] / stats["count"]
        del stats["sum"]  # Remove intermediate sum

    return summary


@router.get("/latest", response_model=dict)
async def get_latest_metrics(
    experiment_id: str,
    db: IResultsDB = Depends(get_db),
) -> dict:
    """
    Get the latest metrics for an experiment.

    Args:
        experiment_id: Experiment ID to get metrics for
        db: Database instance from dependency

    Returns:
        dict: Latest metrics for the experiment

    Raises:
        HTTPException: If experiment is not found
    """
    experiment = db.get_experiment(experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    if experiment.metrics is None:
        return {}

    return experiment.metrics
