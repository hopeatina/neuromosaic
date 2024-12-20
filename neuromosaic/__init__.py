"""
Neuromosaic: Neural Architecture Search with LLM Code Generation.

This package provides tools for:
1. Neural architecture search using LLM-generated code
2. Architecture space exploration
3. Training and evaluation management
4. Results analysis and visualization
"""

__version__ = "0.1.0"
__author__ = "Neuromosaic Team"
__email__ = "team@neuromosaic.ai"

# Avoid circular imports by not importing submodules directly
__all__ = [
    "arch_space",
    "llm_code_gen",
    "env_manager",
    "training_eval",
    "results_db",
    "meta_learning",
    "utils",
    "orchestrator",
]
