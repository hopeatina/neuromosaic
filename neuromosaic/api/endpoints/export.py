"""
Export-related API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
import csv
import io
import json

from neuromosaic.api.dependencies import get_db
from neuromosaic.api.schemas import ExportRequest
from neuromosaic.results_db.interface import IResultsDB

router = APIRouter()


def generate_csv(data: List[dict]) -> StreamingResponse:
    """
    Generate a CSV file from a list of dictionaries.

    Args:
        data: List of dictionaries to convert to CSV

    Returns:
        StreamingResponse: Streaming response containing CSV data
    """
    output = io.StringIO()
    if not data:
        writer = csv.writer(output)
        writer.writerow(["No data available"])
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=export.csv"},
        )

    # Get all possible keys from all dictionaries
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )


@router.post("/")
async def export_data(
    request: ExportRequest,
    db: IResultsDB = Depends(get_db),
) -> StreamingResponse:
    """
    Export experiment data in the requested format.

    Args:
        request: Export request parameters
        db: Database instance from dependency

    Returns:
        StreamingResponse: Streaming response containing exported data

    Raises:
        HTTPException: If format is invalid or data cannot be exported
    """
    # Validate format
    if request.format not in ["json", "csv"]:
        raise HTTPException(
            status_code=400, detail="Invalid format. Must be 'json' or 'csv'"
        )

    # Get experiments
    if request.experiment_ids:
        experiments = [
            db.get_experiment(exp_id)
            for exp_id in request.experiment_ids
            if db.get_experiment(exp_id) is not None
        ]
    else:
        experiments = db.list_experiments()

    # Prepare data for export
    export_data = []
    for exp in experiments:
        data = {
            "id": exp.id,
            "name": exp.name,
            "status": exp.status,
            "created_at": exp.created_at.isoformat(),
            "updated_at": exp.updated_at.isoformat(),
        }

        if request.include_config:
            data["config"] = json.dumps(exp.config)  # Flatten config for CSV

        if request.include_metrics and exp.metrics:
            for metric_name, metric_value in exp.metrics.items():
                data[f"metric_{metric_name}"] = metric_value

        export_data.append(data)

    # Return data in requested format
    if request.format == "json":
        return JSONResponse(content=export_data)
    else:  # CSV
        return generate_csv(export_data)
