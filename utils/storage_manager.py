"""
Storage management utilities for datasets and artifacts.

This module provides functionality for:
1. Fetching and caching datasets
2. Managing model checkpoints and artifacts
3. Handling storage quotas and cleanup
4. Access control for private data

Example:
    >>> from neuramosaic.utils.storage_manager import fetch_dataset
    >>> dataset = fetch_dataset("wikitext-103")
    >>> save_checkpoint(model, metrics, "checkpoints/best.pt")
"""

import os
import shutil
import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from functools import wraps
from datetime import datetime
import requests
import torch
from tqdm import tqdm
from dotenv import load_dotenv

from .logging import setup_logger

logger = setup_logger(__name__)

# Load environment variables for API keys
load_dotenv()


class StorageConfig:
    """Configuration for storage management."""

    # Base directories
    DATA_ROOT = Path("data")
    RAW_DATA = DATA_ROOT / "raw"
    PROCESSED_DATA = DATA_ROOT / "processed"
    EXTERNAL_DATA = DATA_ROOT / "external"
    ARTIFACTS_ROOT = Path("experiments")

    # Cache settings
    CACHE_DIR = Path.home() / ".cache" / "neuramosaic"
    MAX_CACHE_SIZE = 50 * 1024 * 1024 * 1024  # 50GB

    # Chunk size for downloads
    DOWNLOAD_CHUNK_SIZE = 8192  # 8KB

    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        for dir_path in [
            cls.DATA_ROOT,
            cls.RAW_DATA,
            cls.PROCESSED_DATA,
            cls.EXTERNAL_DATA,
            cls.ARTIFACTS_ROOT,
            cls.CACHE_DIR,
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)


class DatasetRegistry:
    """Registry for dataset fetcher functions."""

    _fetchers: Dict[str, callable] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register a dataset fetcher."""

        def decorator(func):
            cls._fetchers[name] = func
            return func

        return decorator

    @classmethod
    def get_fetcher(cls, name: str) -> callable:
        """Get fetcher function for dataset."""
        if name not in cls._fetchers:
            raise ValueError(f"Unknown dataset: {name}")
        return cls._fetchers[name]


def requires_auth(func):
    """Decorator for functions requiring authentication."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = os.getenv("DATASET_API_KEY")
        if not api_key:
            raise ValueError("DATASET_API_KEY not found in environment")
        return func(*args, api_key=api_key, **kwargs)

    return wrapper


def check_storage_quota():
    """Decorator to check storage quota before saving."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_cache_size() > StorageConfig.MAX_CACHE_SIZE:
                cleanup_cache()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_cache_size() -> int:
    """Get total size of cache directory in bytes."""
    total_size = 0
    for dirpath, _, filenames in os.walk(StorageConfig.CACHE_DIR):
        for filename in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, filename))
    return total_size


def cleanup_cache() -> None:
    """Remove oldest files from cache until under quota."""
    files = []
    for dirpath, _, filenames in os.walk(StorageConfig.CACHE_DIR):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            files.append((path, os.path.getmtime(path)))

    # Sort by modification time
    files.sort(key=lambda x: x[1])

    # Remove files until under quota
    while get_cache_size() > StorageConfig.MAX_CACHE_SIZE and files:
        os.remove(files.pop(0)[0])


def compute_file_hash(path: Union[str, Path]) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


@DatasetRegistry.register("wikitext-103")
def fetch_wikitext103(split: str = "train") -> Any:
    """Fetch WikiText-103 dataset."""
    from datasets import load_dataset

    return load_dataset("wikitext", "wikitext-103-v1", split=split)


@check_storage_quota()
def download_dataset(url: str, name: str, force: bool = False) -> Path:
    """
    Download a dataset from URL.

    Args:
        url: Download URL
        name: Dataset name
        force: If True, redownload even if exists

    Returns:
        Path to downloaded file
    """
    target_dir = StorageConfig.EXTERNAL_DATA / name
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = url.split("/")[-1]
    target_path = target_dir / filename

    if target_path.exists() and not force:
        logger.info(f"Dataset {name} already exists")
        return target_path

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
        with open(target_path, "wb") as f:
            for chunk in response.iter_content(StorageConfig.DOWNLOAD_CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    return target_path


def fetch_dataset(name: str, **kwargs) -> Any:
    """
    Fetch a dataset by name.

    Args:
        name: Dataset name
        **kwargs: Arguments for dataset fetcher

    Returns:
        Dataset object
    """
    fetcher = DatasetRegistry.get_fetcher(name)
    return fetcher(**kwargs)


@check_storage_quota()
def save_checkpoint(
    model: torch.nn.Module,
    metrics: Dict[str, float],
    path: Union[str, Path],
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Save a model checkpoint with metrics and metadata.

    Args:
        model: PyTorch model
        metrics: Dictionary of metric values
        path: Save path
        metadata: Optional additional metadata
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = {
        "model_state_dict": model.state_dict(),
        "metrics": metrics,
        "metadata": metadata or {},
        "timestamp": datetime.now().isoformat(),
    }

    torch.save(checkpoint, path)
    logger.info(f"Saved checkpoint to {path}")


def load_checkpoint(
    path: Union[str, Path], model: Optional[torch.nn.Module] = None
) -> Dict[str, Any]:
    """
    Load a checkpoint.

    Args:
        path: Checkpoint path
        model: Optional model to load state into

    Returns:
        Checkpoint dictionary
    """
    checkpoint = torch.load(path)

    if model is not None:
        model.load_state_dict(checkpoint["model_state_dict"])

    return checkpoint


def list_checkpoints(
    experiment_id: str, metric: Optional[str] = None, n_best: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    List checkpoints for an experiment.

    Args:
        experiment_id: Experiment identifier
        metric: Optional metric to sort by
        n_best: Optional number of best checkpoints to return

    Returns:
        List of checkpoint information
    """
    checkpoint_dir = StorageConfig.ARTIFACTS_ROOT / experiment_id / "checkpoints"
    if not checkpoint_dir.exists():
        return []

    checkpoints = []
    for path in checkpoint_dir.glob("*.pt"):
        checkpoint = torch.load(path, map_location="cpu")
        info = {
            "path": path,
            "metrics": checkpoint["metrics"],
            "timestamp": checkpoint["timestamp"],
        }
        checkpoints.append(info)

    if metric is not None:
        checkpoints.sort(key=lambda x: x["metrics"][metric], reverse=True)

    if n_best is not None:
        checkpoints = checkpoints[:n_best]

    return checkpoints


# Initialize directories
StorageConfig.ensure_directories()
