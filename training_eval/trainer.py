"""
Standardized training interface for neural architecture evaluation.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import torch


class Trainer(ABC):
    """
    Abstract base class for model training and evaluation.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def train_model(
        self,
        model: torch.nn.Module,
        train_data: Any,
        val_data: Optional[Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Train a model and return metrics."""
        pass

    @abstractmethod
    async def evaluate_model(
        self, model: torch.nn.Module, test_data: Any, **kwargs
    ) -> Dict[str, Any]:
        """Evaluate a trained model and return metrics."""
        pass
