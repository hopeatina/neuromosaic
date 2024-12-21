# Contributing to Neuromosaic

Thank you for your interest in contributing to Neuromosaic! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Running Experiments](#running-experiments)
5. [Making Changes](#making-changes)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Pull Requests](#pull-requests)

## Code of Conduct

This project follows a standard code of conduct. Please be respectful and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/neuromosaic.git
   cd neuromosaic
   ```
3. Set up the development environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Development Setup

1. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

2. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

3. Configure git:
   ```bash
   git config --local core.autocrlf input
   git config --local core.eol lf
   ```

## Running Experiments

Neuromosaic provides several commands for running and analyzing architecture searches:

### 1. Quick Start

For a quick start with sensible defaults:

```bash
# Basic architecture search
python -m neuromosaic quickstart

# With GPU and parallel execution
python -m neuromosaic quickstart --gpu --batch-size 8

# Customize output directory and use CPU
python -m neuromosaic quickstart --output-dir my_search --cpu --batch-size 4
```

The quickstart command:

- Creates an output directory with a default configuration
- Runs architecture search with proven defaults
- Supports parallel execution with configurable batch size
- Automatically handles async operations
- Shows a summary of the best results

### 2. Custom Experimentation

For more control over the search process:

1. Create a custom configuration file (e.g., `custom_config.yaml`):

   ```yaml
   arch_space:
     dimensions: 64
     bounds:
       num_layers: [2, 8]
       hidden_size: [128, 512]

   search_strategy:
     type: "bayesian_optimization"
     num_trials: 10
     dimensions: 64

   training:
     batch_size: 32
     max_epochs: 5
     learning_rate: 0.001
     optimizer: "adam"
     scheduler: "cosine"
     metrics: ["accuracy", "loss", "latency", "memory_usage"]

   container:
     device: "cpu" # or "gpu"
     memory_limit: "8GB"
     num_cpus: 4
   ```

2. Run the experiment:

   ```bash
   # Run with custom configuration in parallel
   python -m neuromosaic experiment --config custom_config.yaml --output-dir custom_search --batch-size 8

   # Run sequentially
   python -m neuromosaic experiment --config custom_config.yaml --sequential

   # Resume a previous run
   python -m neuromosaic experiment --config custom_config.yaml --resume
   ```

The experiment command supports:

- Parallel or sequential execution
- Configurable batch size for parallel runs
- State saving and resumption
- Custom output directory
- Automatic async operation handling

### 3. Analysis and Visualization

Analyze and compare experiment results:

```bash
# Basic analysis with specific metric
python -m neuromosaic analyze results_dir --metric accuracy

# Compare two experiments with custom format
python -m neuromosaic analyze results_dir --compare-with other_results --format json

# Detailed inspection of specific architecture
python -m neuromosaic inspect <architecture-id> --detailed --export-code
```

Analysis features:

- Multiple output formats (text, JSON, CSV)
- Comparison between experiments
- Detailed metrics visualization
- Code export for specific architectures

### Additional Options

- Set logging level for any command:

  ```bash
  python -m neuromosaic --log-level DEBUG quickstart
  ```

- All commands support `--help` for detailed usage:
  ```bash
  python -m neuromosaic quickstart --help
  python -m neuromosaic experiment --help
  python -m neuromosaic analyze --help
  python -m neuromosaic inspect --help
  ```

The experiment results are stored in the output directory and can be analyzed using the analysis commands. All async operations are handled internally by the commands, making the interface simple and user-friendly.

## Making Changes

1. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Follow the coding style:

   - Use type hints
   - Write docstrings for all public functions/classes
   - Follow PEP 8 guidelines
   - Use async/await for asynchronous code
   - Keep functions focused and small

3. Commit your changes:

   ```bash
   git add .
   git commit -m "feat: description of your changes"
   ```

   Follow conventional commits format:

   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - style: Code style changes
   - refactor: Code refactoring
   - test: Adding tests
   - chore: Maintenance tasks

## Testing

1. Run tests:

   ```bash
   pytest tests/
   python -m pytest tests/ -v
   ```

2. Run type checking:

   ```bash
   mypy neuromosaic/
   ```

3. Run linting:
   ```bash
   black neuromosaic/
   flake8 neuromosaic/
   ```

## Documentation

1. Document all public APIs using Google-style docstrings:

   ```python
   def function(arg1: str, arg2: int) -> bool:
       """
       Short description.

       Longer description if needed.

       Args:
           arg1: Description of arg1
           arg2: Description of arg2

       Returns:
           Description of return value

       Raises:
           ValueError: Description of when this is raised
       """
       pass
   ```

2. Update README.md if adding new features

3. Add examples to docstrings showing common use cases

## Pull Requests

1. Update your branch with main:

   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. Push your changes:

   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a pull request:

   - Use a clear title and description
   - Reference any related issues
   - Include test results
   - Add screenshots for UI changes

4. Respond to review comments

5. Once approved, your PR will be merged

## Adding New Components

### New Search Strategy

1. Create a new file in `orchestrator/strategies/`
2. Implement the `SearchStrategy` interface
3. Add tests in `tests/orchestrator/strategies/`
4. Update strategy documentation

### New LLM Provider

1. Create a new file in `llm_code_gen/providers/`
2. Implement the `CodeGenerator` interface
3. Add provider-specific configuration
4. Add tests and examples

### New Architecture Component

1. Update `arch_space/vector_representation.py`
2. Add encoder/decoder in respective directories
3. Update prompt templates
4. Add tests for the new component

## Questions?

Feel free to:

- Open an issue for discussion
- Ask in the discussions section
- Contact the maintainers

Thank you for contributing to Neuromosaic!
