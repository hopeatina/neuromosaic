# Contributing to Neuramosaic

Thank you for your interest in contributing to Neuramosaic! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Pull Requests](#pull-requests)

## Code of Conduct

This project follows a standard code of conduct. Please be respectful and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/neuramosaic.git
   cd neuramosaic
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
   ```

2. Run type checking:

   ```bash
   mypy neuramosaic/
   ```

3. Run linting:
   ```bash
   black neuramosaic/
   flake8 neuramosaic/
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

Thank you for contributing to Neuramosaic!
