"""
Random search strategy implementation.

This module implements a simple random search strategy that samples architectures
uniformly from the search space. While not sophisticated, random search serves as:
1. A baseline for comparing other strategies
2. An exploration tool for understanding the search space
3. A fallback when other strategies fail

Example:
    >>> config = {"dimensions": 64, "num_samples": 100}
    >>> strategy = RandomSearch(config)
    >>> architecture = await strategy.suggest_architecture()
"""

from typing import Dict, Any, List, Optional
import numpy as np
import logging

from .base_strategy import SearchStrategy
from ...arch_space import ArchitectureVector
from ...utils.logging import setup_logger

logger = setup_logger(__name__)


class RandomSearch(SearchStrategy):
    """
    Random search strategy for architecture exploration.

    This strategy:
    1. Maintains bounds on each dimension
    2. Samples uniformly within those bounds
    3. Tracks the best architectures found

    Attributes:
        dimensions (int): Size of architecture vectors
        bounds (Dict[str, tuple]): Min/max values for each dimension
        num_samples (int): Total number of samples to generate
        current_sample (int): Number of samples generated so far
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the random search strategy.

        Args:
            config: Dictionary containing:
                - dimensions: Size of architecture vectors
                - bounds: Min/max values for dimensions
                - num_samples: Total samples to generate
        """
        super().__init__(config)
        self.dimensions = config["dimensions"]
        self.bounds = config.get("bounds", {})
        self.num_samples = config.get("num_samples", float("inf"))
        self.current_sample = 0

    def _setup_search_space(self) -> None:
        """Initialize search space bounds from configuration."""
        if not self.bounds:
            self.bounds = {f"dim_{i}": (0.0, 1.0) for i in range(self.dimensions)}

    async def suggest_architecture(self) -> ArchitectureVector:
        """
        Generate a random architecture vector.

        Returns:
            ArchitectureVector with random values

        Raises:
            SearchSpaceExhausted: If num_samples is reached
        """
        if self.current_sample >= self.num_samples:
            raise SearchSpaceExhausted(f"Reached maximum samples: {self.num_samples}")

        vector = ArchitectureVector(self.dimensions)
        for i, (min_val, max_val) in enumerate(self.bounds.values()):
            vector.vector[i] = np.random.uniform(min_val, max_val)

        self.current_sample += 1
        return vector

    async def update_with_results(
        self, architecture: ArchitectureVector, results: Dict[str, float]
    ) -> None:
        """
        Record results in history.

        Args:
            architecture: The evaluated architecture
            results: Dictionary of metric values
        """
        self.history.append(
            {
                "architecture": architecture,
                "results": results,
                "sample_num": self.current_sample,
            }
        )

    async def get_best_architectures(
        self, metric: str, num_architectures: int = 1
    ) -> List[ArchitectureVector]:
        """
        Get the best architectures by metric value.

        Args:
            metric: Name of the metric to sort by
            num_architectures: Number of top architectures to return

        Returns:
            List of best architectures
        """
        if not self.history:
            return []

        sorted_history = sorted(
            self.history, key=lambda x: x["results"][metric], reverse=True
        )

        return [h["architecture"] for h in sorted_history[:num_architectures]]


class SearchSpaceExhausted(Exception):
    """Raised when the search strategy cannot generate more samples."""

    pass
