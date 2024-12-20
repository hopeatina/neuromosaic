"""
Base interface for architecture search strategies.

This module defines the common interface that all search strategies must implement.
Strategies can range from simple random search to sophisticated Bayesian optimization
or evolutionary algorithms.

Example:
    >>> strategy = RandomSearch(config)
    >>> arch_vector = await strategy.suggest_architecture()
    >>> results = {"accuracy": 0.85, "latency": 120}
    >>> await strategy.update_with_results(arch_vector, results)
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import numpy as np
import logging

from ...arch_space import ArchitectureVector
from ...utils.logging import setup_logger

logger = setup_logger(__name__)


class SearchStrategy(ABC):
    """
    Abstract base class for architecture search strategies.

    A search strategy is responsible for:
    1. Suggesting new architectures to evaluate
    2. Processing results from evaluations
    3. Learning from past results to improve suggestions
    4. Maintaining search state and history

    Attributes:
        config (Dict[str, Any]): Configuration containing:
            - search_space: Definition of the architecture space
            - optimization_objectives: Metrics to optimize
            - constraints: Any constraints on architectures
        history (List[Dict[str, Any]]): History of evaluated architectures
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the search strategy.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.history = []
        self._setup_search_space()

    def _setup_search_space(self) -> None:
        """Initialize the search space from configuration."""
        raise NotImplementedError

    @abstractmethod
    async def suggest_architecture(self) -> ArchitectureVector:
        """
        Suggest the next architecture to evaluate.

        The suggestion process should:
        1. Consider the history of evaluations
        2. Balance exploration and exploitation
        3. Respect any constraints

        Returns:
            An ArchitectureVector instance

        Raises:
            SearchSpaceExhausted: If no valid architectures remain
        """
        pass

    @abstractmethod
    async def update_with_results(
        self, architecture: ArchitectureVector, results: Dict[str, float]
    ) -> None:
        """
        Update strategy with results from an evaluation.

        Args:
            architecture: The evaluated architecture
            results: Dictionary of metric values
        """
        pass

    @abstractmethod
    async def get_best_architectures(
        self, metric: str, num_architectures: int = 1
    ) -> List[ArchitectureVector]:
        """
        Get the best architectures found so far.

        Args:
            metric: Name of the metric to optimize
            num_architectures: Number of top architectures to return

        Returns:
            List of best architectures sorted by metric
        """
        pass

    def save_state(self, path: str) -> None:
        """
        Save the strategy's state to disk.

        Args:
            path: Path to save the state file
        """
        raise NotImplementedError

    def load_state(self, path: str) -> None:
        """
        Load the strategy's state from disk.

        Args:
            path: Path to the state file
        """
        raise NotImplementedError
