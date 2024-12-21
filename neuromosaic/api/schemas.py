"""
Pydantic models for request/response validation.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ExperimentBase(BaseModel):
    """Base experiment model."""

    name: str = Field(..., description="Name of the experiment")
    description: Optional[str] = Field(None, description="Optional description")
    config: Dict[str, Any] = Field(..., description="Experiment configuration")


class ExperimentCreate(ExperimentBase):
    """Model for creating a new experiment."""

    pass


class Experiment(ExperimentBase):
    """Model for experiment responses."""

    id: str = Field(..., description="Unique experiment identifier")
    status: str = Field(..., description="Current experiment status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    metrics: Optional[Dict[str, float]] = Field(None, description="Latest metrics")

    class Config:
        """Pydantic config."""

        from_attributes = True


class ArchitectureBase(BaseModel):
    """Base architecture model."""

    name: str = Field(..., description="Architecture name")
    description: Optional[str] = Field(None, description="Architecture description")
    spec: Dict[str, Any] = Field(..., description="Architecture specification")


class Architecture(ArchitectureBase):
    """Model for architecture responses."""

    id: str = Field(..., description="Unique architecture identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True


class MetricResponse(BaseModel):
    """Model for metric responses."""

    experiment_id: str = Field(..., description="Associated experiment ID")
    metrics: Dict[str, float] = Field(..., description="Metric values")
    timestamp: datetime = Field(..., description="Metric timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True


class ExportRequest(BaseModel):
    """Model for export requests."""

    experiment_ids: Optional[List[str]] = Field(
        None, description="Optional list of experiment IDs to export"
    )
    format: str = Field("json", description="Export format (json or csv)")
    include_metrics: bool = Field(
        True, description="Whether to include metrics in export"
    )
    include_config: bool = Field(
        True, description="Whether to include configurations in export"
    )
