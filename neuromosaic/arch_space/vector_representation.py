"""
Vector representation of neural architectures.

This module provides the core functionality for encoding and decoding neural
architectures as continuous vectors. The vector space representation enables:
- Smooth interpolation between architectures
- Gradient-based optimization
- Distance metrics between architectures
- Clustering and visualization

Example:
    >>> arch_vector = ArchitectureVector(dimensions=64)
    >>> arch_spec = {
    ...     "num_layers": 4,
    ...     "hidden_size": 256,
    ...     "num_heads": 8,
    ...     "ffn_type": "gated"
    ... }
    >>> arch_vector.encode(arch_spec)
    >>> mutated = arch_vector.mutate(mutation_rate=0.1)
    >>> new_spec = mutated.decode()
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import logging

from ..utils.logging import setup_logger

logger = setup_logger(__name__)


@dataclass
class ArchSpace:
    """
    Configuration for the architecture search space.

    Attributes:
        dimensions: Size of architecture vectors
        bounds: Valid ranges for continuous parameters
        categorical_dims: Valid values for categorical parameters
    """

    dimensions: int = 64
    bounds: Dict[str, Tuple[float, float]] = None
    categorical_dims: Dict[str, List[str]] = None

    def __post_init__(self):
        """Initialize default bounds and categorical dimensions if not provided."""
        if self.bounds is None:
            self.bounds = {
                "num_layers": (2, 12),
                "hidden_size": (128, 1024),
                "num_heads": (4, 16),
                "ffn_ratio": (2.0, 8.0),
            }

        if self.categorical_dims is None:
            self.categorical_dims = {
                "ffn_type": ["vanilla", "gated", "expert"],
                "attention_type": ["vanilla", "linear", "sparse"],
                "norm_type": ["layer", "rmsnorm"],
                "activation": ["relu", "gelu", "swish"],
            }

    def create_vector(self) -> "ArchitectureVector":
        """Create a new architecture vector with this space's configuration."""
        return ArchitectureVector(
            dimensions=self.dimensions,
            bounds=self.bounds,
            categorical_dims=self.categorical_dims,
        )


@dataclass
class ArchitectureSpec:
    """
    Structured representation of an architecture specification.

    Attributes:
        num_layers: Number of transformer layers
        hidden_size: Model dimension
        num_heads: Number of attention heads
        ffn_type: Type of feed-forward network
        activation: Activation function
        norm_type: Type of normalization
        dropout: Dropout rate
    """

    num_layers: int
    hidden_size: int
    num_heads: int
    ffn_type: str
    activation: str = "gelu"
    norm_type: str = "layer_norm"
    dropout: float = 0.1


class ArchitectureVector:
    """
    Represents a neural architecture as a continuous vector in a defined search space.

    The vector space is structured to capture both discrete and continuous
    architectural choices. Categorical variables are encoded using a
    learned embedding or one-hot encoding.

    Attributes:
        dimensions (int): Size of the vector representation
        vector (np.ndarray): The actual vector values
        bounds (Dict[str, Tuple[float, float]]): Valid ranges for each dimension
        categorical_dims (Dict[str, List[str]]): Valid values for categorical dimensions
    """

    def __init__(
        self,
        dimensions: int,
        bounds: Optional[Dict[str, Tuple[float, float]]] = None,
        categorical_dims: Optional[Dict[str, List[str]]] = None,
    ):
        """
        Initialize an architecture vector.

        Args:
            dimensions: Size of the vector
            bounds: Dictionary mapping dimension names to (min, max) ranges
            categorical_dims: Dictionary mapping categorical dimension names
                to lists of valid values
        """
        self.dimensions = dimensions
        self.bounds = bounds or {}
        self.categorical_dims = categorical_dims or {}

        # Calculate required dimensions
        required_dims = len(self.bounds)  # One dimension per continuous parameter
        for choices in self.categorical_dims.values():
            required_dims += len(
                choices
            )  # One-hot encoding size for each categorical parameter

        if required_dims > dimensions:
            raise ValueError(
                f"Vector dimensions {dimensions} too small for encoding size {required_dims}"
            )

        # Initialize vector with zeros
        self.vector = np.zeros(dimensions)

    def encode(self, arch_spec: Dict[str, Any]) -> None:
        """
        Encode an architecture specification into a vector representation.

        The encoding process:
        1. Maps continuous values (e.g., hidden size) to normalized ranges
        2. Converts categorical choices to one-hot or learned embeddings
        3. Ensures all values are within valid bounds

        Args:
            arch_spec: Dictionary containing architecture parameters

        Raises:
            ValueError: If specification contains invalid values
        """
        # Initialize vector with zeros
        self.vector = np.zeros(self.dimensions)
        current_idx = 0

        # Handle continuous dimensions
        for param, (min_val, max_val) in self.bounds.items():
            value = arch_spec.get(param)
            if value is None:
                # Use midpoint as default
                value = (min_val + max_val) / 2
            elif not min_val <= value <= max_val:
                raise ValueError(
                    f"{param} value {value} is outside bounds [{min_val}, {max_val}]"
                )
            # Normalize to [0, 1]
            self.vector[current_idx] = (value - min_val) / (max_val - min_val)
            current_idx += 1

        # Handle categorical dimensions
        for param, choices in self.categorical_dims.items():
            value = arch_spec.get(param)
            if value is None:
                # Use first choice as default
                value = choices[0]
            elif value not in choices:
                raise ValueError(
                    f"Invalid {param} value: {value}. Must be one of {choices}"
                )
            # One-hot encoding
            choice_idx = choices.index(value)
            one_hot = np.zeros(len(choices))
            one_hot[choice_idx] = 1.0  # Use 1.0 instead of 1 for consistent float type
            self.vector[current_idx : current_idx + len(choices)] = one_hot
            current_idx += len(choices)

    def decode(self) -> Dict[str, Any]:
        """
        Decode the vector representation back into an architecture specification.

        The decoding process:
        1. Maps normalized values back to their original ranges
        2. Converts one-hot encodings back to categorical choices
        3. Ensures all values are valid

        Returns:
            Dictionary containing architecture parameters
        """
        if self.vector is None:
            raise ValueError("Vector not initialized. Call encode() first.")

        arch_spec = {}
        current_idx = 0

        # Handle continuous dimensions
        for param, (min_val, max_val) in self.bounds.items():
            # Denormalize from [0, 1]
            value = self.vector[current_idx] * (max_val - min_val) + min_val
            # Round integer parameters
            if isinstance(min_val, int) and isinstance(max_val, int):
                value = round(value)
            arch_spec[param] = value
            current_idx += 1

        # Handle categorical dimensions
        for param, choices in self.categorical_dims.items():
            one_hot = self.vector[current_idx : current_idx + len(choices)]
            # Get the index of the maximum value
            choice_idx = int(
                np.argmax(one_hot)
            )  # Convert to int for consistent indexing
            # Ensure the one-hot encoding is valid (has a clear maximum)
            if (
                np.sum(one_hot > 0.9) != 1
            ):  # Check if there's exactly one strong activation
                logger.warning(f"Ambiguous one-hot encoding for {param}: {one_hot}")
                # Use the first choice as default if encoding is ambiguous
                choice_idx = 0
            arch_spec[param] = choices[choice_idx]
            current_idx += len(choices)

        return arch_spec

    def mutate(self, mutation_rate: float = 0.1) -> "ArchitectureVector":
        """
        Create a mutated copy of this architecture vector.

        The mutation process:
        1. Randomly perturbs continuous values within bounds
        2. Randomly changes categorical choices
        3. Ensures mutation rate controls frequency of changes

        Args:
            mutation_rate: Probability of each dimension being mutated

        Returns:
            New ArchitectureVector instance with mutated values
        """
        if self.vector is None:
            raise ValueError("Vector not initialized. Call encode() first.")

        # Create a copy of the current vector
        mutated = ArchitectureVector(
            dimensions=self.dimensions,
            bounds=self.bounds,
            categorical_dims=self.categorical_dims,
        )
        mutated.vector = self.vector.copy()

        # Determine which dimensions to mutate
        mutation_mask = np.random.random(self.dimensions) < mutation_rate

        current_idx = 0

        # Mutate continuous dimensions
        for _ in self.bounds:
            if mutation_mask[current_idx]:
                # Add random noise, clip to [0, 1]
                noise = np.random.normal(0, 0.1)
                mutated.vector[current_idx] = np.clip(
                    mutated.vector[current_idx] + noise, 0, 1
                )
            current_idx += 1

        # Mutate categorical dimensions
        for _, choices in self.categorical_dims.items():
            n_choices = len(choices)
            if any(mutation_mask[current_idx : current_idx + n_choices]):
                # Randomly select a new choice
                new_choice = np.zeros(n_choices)
                new_choice[np.random.randint(n_choices)] = 1
                mutated.vector[current_idx : current_idx + n_choices] = new_choice
            current_idx += n_choices

        return mutated

    def crossover(
        self, other: "ArchitectureVector", crossover_points: Optional[List[int]] = None
    ) -> Tuple["ArchitectureVector", "ArchitectureVector"]:
        """
        Perform crossover with another architecture vector.

        The crossover process:
        1. Validates compatibility of vectors
        2. Performs uniform or multi-point crossover
        3. Ensures valid combinations for categorical dimensions

        Args:
            other: Another ArchitectureVector instance
            crossover_points: Optional list of crossover indices

        Returns:
            Two new ArchitectureVector instances containing mixed genes

        Raises:
            ValueError: If vectors have different dimensions
        """
        if self.vector is None or other.vector is None:
            raise ValueError("Both vectors must be initialized before crossover.")

        if self.dimensions != other.dimensions:
            raise ValueError("Cannot crossover vectors with different dimensions.")

        # Create children
        child1 = ArchitectureVector(
            dimensions=self.dimensions,
            bounds=self.bounds,
            categorical_dims=self.categorical_dims,
        )
        child2 = ArchitectureVector(
            dimensions=self.dimensions,
            bounds=self.bounds,
            categorical_dims=self.categorical_dims,
        )

        # Initialize with parent vectors
        child1.vector = self.vector.copy()
        child2.vector = other.vector.copy()

        if crossover_points is None:
            # Perform uniform crossover
            mask = np.random.random(self.dimensions) < 0.5
            child1.vector = np.where(mask, self.vector, other.vector)
            child2.vector = np.where(mask, other.vector, self.vector)
        else:
            # Perform multi-point crossover
            crossover_points = sorted(crossover_points)
            swap = False
            start = 0
            for point in crossover_points:
                if swap:
                    child1.vector[start:point] = other.vector[start:point]
                    child2.vector[start:point] = self.vector[start:point]
                swap = not swap
                start = point

        # Fix categorical dimensions to ensure one-hot encoding
        current_idx = len(self.bounds)
        for _, choices in self.categorical_dims.items():
            n_choices = len(choices)
            # For each child, ensure exactly one choice is selected
            for child in [child1, child2]:
                one_hot = child.vector[current_idx : current_idx + n_choices]
                max_idx = np.argmax(one_hot)
                one_hot.fill(0)
                one_hot[max_idx] = 1
                child.vector[current_idx : current_idx + n_choices] = one_hot
            current_idx += n_choices

        return child1, child2

    def distance(self, other: "ArchitectureVector") -> float:
        """
        Calculate distance to another architecture vector.

        The distance metric:
        1. Uses Euclidean distance for continuous dimensions
        2. Uses Hamming distance for categorical dimensions
        3. Normalizes and combines both distances

        Args:
            other: Another ArchitectureVector instance

        Returns:
            Float distance value

        Raises:
            ValueError: If vectors have different dimensions or are not initialized
        """
        if self.vector is None or other.vector is None:
            raise ValueError(
                "Both vectors must be initialized before calculating distance."
            )

        if self.dimensions != other.dimensions:
            raise ValueError(
                "Cannot calculate distance between vectors with different dimensions."
            )

        # Initialize distance components
        continuous_dist = 0.0
        categorical_dist = 0.0

        current_idx = 0

        # Calculate distance for continuous dimensions
        for _ in self.bounds:
            diff = self.vector[current_idx] - other.vector[current_idx]
            continuous_dist += diff * diff
            current_idx += 1

        # Calculate distance for categorical dimensions
        for _, choices in self.categorical_dims.items():
            n_choices = len(choices)
            # Compare one-hot encodings
            v1 = self.vector[current_idx : current_idx + n_choices]
            v2 = other.vector[current_idx : current_idx + n_choices]
            # Use Hamming distance (number of differing positions)
            categorical_dist += (
                np.sum(v1 != v2) / 2
            )  # Divide by 2 since each difference counts twice
            current_idx += n_choices

        # Normalize and combine distances
        if self.bounds:
            continuous_dist = np.sqrt(continuous_dist) / np.sqrt(len(self.bounds))
        if self.categorical_dims:
            categorical_dist /= len(self.categorical_dims)

        # Weight both components equally
        return (
            (continuous_dist + categorical_dist) / 2
            if self.bounds and self.categorical_dims
            else continuous_dist if self.bounds else categorical_dist
        )
