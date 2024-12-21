"""
Interface for experiment results database.

This module defines the interface for storing and retrieving experiment results.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime


class IResultsDB(ABC):
    """
    Interface for experiment results database operations.
    This interface is used by the API to ensure consistent data access.
    """

    @abstractmethod
    def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """
        Get experiment details by ID.

        Args:
            experiment_id: Unique identifier for the experiment

        Returns:
            Optional[Dict[str, Any]]: Experiment details or None if not found
        """
        pass

    @abstractmethod
    def list_experiments(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List experiments with pagination.

        Args:
            skip: Number of experiments to skip
            limit: Maximum number of experiments to return

        Returns:
            List[Dict[str, Any]]: List of experiment details
        """
        pass

    @abstractmethod
    def create_experiment(
        self, name: str, description: Optional[str], config: Dict[str, Any]
    ) -> str:
        """
        Create a new experiment.

        Args:
            name: Name of the experiment
            description: Optional description
            config: Experiment configuration

        Returns:
            str: ID of the created experiment
        """
        pass

    @abstractmethod
    def delete_experiment(self, experiment_id: str) -> bool:
        """
        Delete an experiment.

        Args:
            experiment_id: Unique identifier for the experiment

        Returns:
            bool: True if deleted, False if not found
        """
        pass

    @abstractmethod
    def get_metrics(
        self,
        experiment_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        metric_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get metrics with optional filtering.

        Args:
            experiment_id: Optional experiment ID to filter by
            start_time: Optional start time for filtering
            end_time: Optional end time for filtering
            metric_names: Optional list of metric names to filter by

        Returns:
            List[Dict[str, Any]]: List of metrics
        """
        pass

    @abstractmethod
    def get_architecture(self, architecture_id: str) -> Optional[Dict[str, Any]]:
        """
        Get architecture details by ID.

        Args:
            architecture_id: Unique identifier for the architecture

        Returns:
            Optional[Dict[str, Any]]: Architecture details or None if not found
        """
        pass

    @abstractmethod
    def list_architectures(
        self, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List architectures with pagination.

        Args:
            skip: Number of architectures to skip
            limit: Maximum number of architectures to return

        Returns:
            List[Dict[str, Any]]: List of architecture details
        """
        pass
