"""
Architecture encoder instance management.

This module provides functions to get and manage architecture encoder instances.
"""

from typing import Optional, Dict, Any
import logging

from .vector_representation import IArchitectureEncoder, ArchSpace
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

_encoder_instance: Optional[IArchitectureEncoder] = None


def get_encoder_instance(
    config: Optional[Dict[str, Any]] = None
) -> IArchitectureEncoder:
    """
    Get or create an architecture encoder instance.

    Args:
        config: Optional configuration for the encoder

    Returns:
        IArchitectureEncoder: An instance of the architecture encoder
    """
    global _encoder_instance

    if _encoder_instance is None:
        # Create default config if none provided
        if config is None:
            config = {
                "dimensions": 64,
                "bounds": {
                    "num_layers": (2, 8),
                    "hidden_size": (128, 512),
                },
                "categorical_dims": {
                    "activation": ["relu", "gelu", "swish"],
                    "norm_type": ["layer_norm", "batch_norm"],
                },
            }

        # Create arch space from config
        arch_space = ArchSpace(
            dimensions=config.get("dimensions", 64),
            bounds=config.get("bounds"),
            categorical_dims=config.get("categorical_dims"),
        )

        # Create encoder instance using existing functionality
        # This will be implemented based on the existing architecture space implementation
        _encoder_instance = arch_space

    return _encoder_instance
