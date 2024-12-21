"""
Orchestrator interface for experiment management.

This module defines the interface for the experiment orchestrator,
which is responsible for managing and running experiments.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class IOrchestrator(ABC):
    """
    Interface for experiment orchestration.
    This interface is used by the API to ensure consistent experiment management.
    """

    @abstractmethod
    def schedule_experiment(self, experiment_id: str) -> None:
        """
        Schedule a new experiment for execution.

        Args:
            experiment_id: Unique identifier for the experiment
        """
        pass

    @abstractmethod
    def stop_experiment(self, experiment_id: str) -> None:
        """
        Stop a running experiment.

        Args:
            experiment_id: Unique identifier for the experiment
        """
        pass

    @abstractmethod
    def get_experiment_status(self, experiment_id: str) -> Dict[str, Any]:
        """
        Get the current status of an experiment.

        Args:
            experiment_id: Unique identifier for the experiment

        Returns:
            Dict[str, Any]: Status information including state, progress, etc.
        """
        pass

    @abstractmethod
    def list_running_experiments(self) -> List[str]:
        """
        Get a list of currently running experiment IDs.

        Returns:
            List[str]: List of experiment IDs
        """
        pass

    @abstractmethod
    def get_experiment_logs(
        self, experiment_id: str, start_time: Optional[str] = None
    ) -> List[str]:
        """
        Get logs for a specific experiment.

        Args:
            experiment_id: Unique identifier for the experiment
            start_time: Optional timestamp to get logs from

        Returns:
            List[str]: List of log entries
        """
        pass
