"""
Interface for LLM-based code generation.

This module defines the interfaces for converting architecture specifications
into executable PyTorch code using Large Language Models. It supports:
- Multiple LLM providers (local LLaMA, OpenAI, etc.)
- Customizable prompt templates
- Code validation and testing
- Fallback strategies for failed generations

Example:
    >>> config = {"model": "gpt-4", "temperature": 0.7}
    >>> generator = OpenAICodeGenerator(config)
    >>> arch_spec = {"num_layers": 4, "hidden_size": 256}
    >>> code = await generator.generate_code(arch_spec)
    >>> is_valid = await generator.validate_code(code)
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import logging
from pathlib import Path

from ..utils.logging import setup_logger

logger = setup_logger(__name__)


class PromptTemplate(ABC):
    """
    Abstract base class for prompt templates.

    A prompt template converts an architecture specification into
    a natural language prompt for the LLM.

    Attributes:
        template_path (Path): Path to the prompt template file
        variables (Dict[str, str]): Template variable mappings
    """

    def __init__(self, template_path: Optional[Path] = None):
        """
        Initialize the prompt template.

        Args:
            template_path: Optional path to a template file
        """
        self.template_path = template_path
        self.variables = {}

    @abstractmethod
    def build_prompt(self, arch_spec: Dict[str, Any]) -> str:
        """
        Build a prompt from an architecture specification.

        Args:
            arch_spec: Dictionary containing architecture parameters

        Returns:
            Formatted prompt string for the LLM
        """
        pass

    @abstractmethod
    def parse_response(self, response: str) -> str:
        """
        Extract code from LLM response.

        Args:
            response: Raw LLM response text

        Returns:
            Clean Python code string

        Raises:
            ValueError: If response doesn't contain valid code
        """
        pass


class CodeGenerator(ABC):
    """
    Abstract base class for LLM-based code generation.

    Handles the end-to-end process of:
    1. Converting architecture specs to prompts
    2. Sending prompts to LLM
    3. Processing and validating responses
    4. Handling errors and retries

    Attributes:
        config (Dict[str, Any]): Configuration containing:
            - model: Name/path of the LLM to use
            - temperature: Sampling temperature
            - max_tokens: Maximum response length
            - retry_config: Settings for retries
        prompt_template (PromptTemplate): Template for generating prompts
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the code generator.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self._setup_template()

    def _setup_template(self) -> None:
        """Initialize the prompt template from configuration."""
        raise NotImplementedError

    @abstractmethod
    async def generate_code(
        self, arch_spec: Dict[str, Any], max_retries: int = 3
    ) -> str:
        """
        Generate code from an architecture specification.

        The generation process:
        1. Convert spec to prompt using template
        2. Send prompt to LLM
        3. Extract and validate code from response
        4. Retry with modifications if generation fails

        Args:
            arch_spec: Dictionary containing architecture parameters
            max_retries: Maximum number of generation attempts

        Returns:
            String containing valid Python code

        Raises:
            GenerationError: If code generation fails after retries
        """
        pass

    @abstractmethod
    async def validate_code(
        self, code: str, validation_tests: Optional[List[str]] = None
    ) -> bool:
        """
        Validate generated code for syntax and basic correctness.

        Validation steps:
        1. Check Python syntax
        2. Verify imports and dependencies
        3. Run basic sanity checks
        4. Execute validation tests if provided

        Args:
            code: String containing Python code
            validation_tests: Optional list of test cases

        Returns:
            True if code passes all validation
        """
        pass

    @abstractmethod
    async def repair_code(self, code: str, error_message: str) -> str:
        """
        Attempt to fix invalid generated code.

        Args:
            code: The invalid code string
            error_message: Description of the error

        Returns:
            Fixed code string

        Raises:
            RepairError: If code cannot be fixed
        """
        pass
