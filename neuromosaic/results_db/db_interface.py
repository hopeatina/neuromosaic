"""
Database interface for experiment results storage and retrieval.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class ResultsDB(ABC):
    """
    Abstract base class for results database operations.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def save_run_info(self, run_info: Dict[str, Any]) -> str:
        """Save information about an experiment run."""
        pass

    @abstractmethod
    async def get_best_architectures(
        self, metric: str, limit: int = 10, **filters
    ) -> List[Dict[str, Any]]:
        """Get the best performing architectures based on a metric."""
        pass

    @abstractmethod
    async def list_all_runs(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **filters
    ) -> List[Dict[str, Any]]:
        """List all experiment runs with optional filtering."""
        pass
