"""Setup configuration for Neuromosaic package."""

from setuptools import setup, find_packages

setup(
    name="neuromosaic",
    version="0.1.0",
    description="Neural Architecture Search with LLM Code Generation",
    author="Neuromosaic Team",
    author_email="team@neuromosaic.ai",
    packages=find_packages(include=["neuromosaic", "neuromosaic.*"]),
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "pyyaml>=5.4.0",
        "click>=8.0.0",
        "tqdm>=4.62.0",
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
        "wandb>=0.12.0",
        "datasets>=2.0.0",
        "docker>=5.0.0",
        "psycopg2-binary>=2.9.0",
        "sqlalchemy>=1.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.16.0",
            "pytest-cov>=2.12.0",
            "black>=22.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "isort>=5.9.0",
            "pre-commit>=2.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "neuromosaic=neuromosaic.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
