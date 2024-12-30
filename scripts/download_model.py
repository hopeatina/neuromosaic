#!/usr/bin/env python3
"""
Script to download LLaMA model for code generation.
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from tqdm import tqdm


def download_file(url: str, dest_path: Path, chunk_size: int = 8192) -> None:
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    with open(dest_path, "wb") as f, tqdm(
        desc=dest_path.name,
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=chunk_size):
            size = f.write(data)
            pbar.update(size)


def main():
    parser = argparse.ArgumentParser(
        description="Download LLaMA model for code generation"
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="models",
        help="Directory to save the model (default: models)",
    )
    args = parser.parse_args()

    model_dir = Path(args.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "llama-2-7b-chat.gguf"
    if model_path.exists():
        print(f"Model already exists at {model_path}")
        sys.exit(0)

    # URL for the LLaMA model
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"

    print(f"Downloading model to {model_path}...")
    try:
        download_file(model_url, model_path)
        print("Download complete!")
    except Exception as e:
        print(f"Error downloading model: {e}")
        if model_path.exists():
            model_path.unlink()
        sys.exit(1)


if __name__ == "__main__":
    main()
