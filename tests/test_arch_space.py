"""
Tests for the architecture space module.
"""

import pytest
import numpy as np
from typing import Dict, Any

from neuromosaic.arch_space import ArchitectureVector
from neuromosaic.arch_space.vector_representation import ArchitectureSpec


@pytest.fixture
def arch_spec() -> Dict[str, Any]:
    """Provide a sample architecture specification."""
    return {
        "num_layers": 4,
        "hidden_size": 256,
        "num_heads": 8,
        "ffn_type": "gated",
        "activation": "gelu",
        "norm_type": "layer_norm",
        "dropout": 0.1,
    }


@pytest.fixture
def vector_config() -> Dict[str, Any]:
    """Provide configuration for architecture vectors."""
    return {
        "dimensions": 16,
        "bounds": {
            "num_layers": (2, 12),
            "hidden_size": (128, 1024),
            "num_heads": (4, 16),
            "dropout": (0.0, 0.5),
        },
        "categorical_dims": {
            "ffn_type": ["vanilla", "gated", "expert"],
            "attention_type": ["vanilla", "linear", "sparse"],
            "norm_type": ["layer_norm", "rmsnorm"],
            "activation": ["relu", "gelu", "swish"],
        },
    }


def test_architecture_spec():
    """Test the ArchitectureSpec dataclass."""
    spec = ArchitectureSpec(
        num_layers=4, hidden_size=256, num_heads=8, ffn_type="gated"
    )

    assert spec.num_layers == 4
    assert spec.hidden_size == 256
    assert spec.num_heads == 8
    assert spec.ffn_type == "gated"
    assert spec.activation == "gelu"  # default value
    assert spec.norm_type == "layer_norm"  # default value
    assert spec.dropout == 0.1  # default value


def test_architecture_vector_initialization(vector_config: Dict[str, Any]):
    """Test initializing an architecture vector."""
    vector = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )

    assert vector.dimensions == vector_config["dimensions"]
    assert vector.bounds == vector_config["bounds"]
    assert vector.categorical_dims == vector_config["categorical_dims"]
    assert np.all(vector.vector == 0)


def test_encode_decode_roundtrip(
    vector_config: Dict[str, Any], arch_spec: Dict[str, Any]
):
    """Test encoding and decoding an architecture specification."""
    vector = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )

    # Encode the specification
    vector.encode(arch_spec)

    # Decode back to specification
    decoded_spec = vector.decode()

    # Check continuous values are approximately equal
    assert abs(decoded_spec["num_layers"] - arch_spec["num_layers"]) <= 1
    assert abs(decoded_spec["hidden_size"] - arch_spec["hidden_size"]) <= 32
    assert abs(decoded_spec["num_heads"] - arch_spec["num_heads"]) <= 1

    # Check categorical values match exactly
    assert decoded_spec["ffn_type"] == arch_spec["ffn_type"]
    assert decoded_spec["activation"] == arch_spec["activation"]
    assert decoded_spec["norm_type"] == arch_spec["norm_type"]


def test_mutation(vector_config: Dict[str, Any], arch_spec: Dict[str, Any]):
    """Test mutating an architecture vector."""
    vector = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )
    vector.encode(arch_spec)

    # Store original vector
    original = vector.vector.copy()

    # Mutate with high rate to ensure changes
    mutated = vector.mutate(mutation_rate=1.0)

    # Verify vectors are different
    assert not np.all(mutated.vector == original)

    # Verify bounds are respected
    for dim, (min_val, max_val) in vector_config["bounds"].items():
        decoded = mutated.decode()
        assert min_val <= decoded[dim] <= max_val

    # Verify categorical values are valid
    for dim, valid_values in vector_config["categorical_dims"].items():
        decoded = mutated.decode()
        assert decoded[dim] in valid_values


def test_crossover(vector_config: Dict[str, Any]):
    """Test crossover between two architecture vectors."""
    parent1 = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )
    parent2 = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )

    # Initialize with different random values
    parent1.vector = np.random.rand(vector_config["dimensions"])
    parent2.vector = np.random.rand(vector_config["dimensions"])

    # Perform crossover
    child1, child2 = parent1.crossover(parent2)

    # Verify children are different from parents
    assert not np.all(child1.vector == parent1.vector)
    assert not np.all(child2.vector == parent2.vector)

    # Verify children have valid values
    for child in [child1, child2]:
        decoded = child.decode()
        for dim, (min_val, max_val) in vector_config["bounds"].items():
            assert min_val <= decoded[dim] <= max_val
        for dim, valid_values in vector_config["categorical_dims"].items():
            assert decoded[dim] in valid_values


def test_distance_calculation(vector_config: Dict[str, Any]):
    """Test calculating distance between architecture vectors."""
    vector1 = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )
    vector2 = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )

    # Initialize with identical values
    same_values = np.random.rand(vector_config["dimensions"])
    vector1.vector = same_values
    vector2.vector = same_values.copy()

    # Distance to self should be 0
    assert vector1.distance(vector2) == 0

    # Modify second vector
    vector2.vector += 0.1

    # Distance should be positive
    assert vector1.distance(vector2) > 0

    # Distance should be symmetric
    assert vector1.distance(vector2) == vector2.distance(vector1)


def test_invalid_specification(vector_config: Dict[str, Any]):
    """Test handling of invalid architecture specifications."""
    vector = ArchitectureVector(
        dimensions=vector_config["dimensions"],
        bounds=vector_config["bounds"],
        categorical_dims=vector_config["categorical_dims"],
    )

    # Test invalid continuous value
    invalid_spec = {
        "num_layers": -1,  # Invalid: negative layers
        "hidden_size": 256,
        "num_heads": 8,
        "ffn_type": "gated",
    }
    with pytest.raises(ValueError):
        vector.encode(invalid_spec)

    # Test invalid categorical value
    invalid_spec = {
        "num_layers": 4,
        "hidden_size": 256,
        "num_heads": 8,
        "ffn_type": "invalid_type",  # Invalid: unknown type
    }
    with pytest.raises(ValueError):
        vector.encode(invalid_spec)
