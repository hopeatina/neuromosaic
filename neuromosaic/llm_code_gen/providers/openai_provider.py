"""
OpenAI-specific implementation of the code generation interface.
"""

import ast
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

import openai
from openai import AsyncOpenAI

from ..codegen_interface import CodeGenerator, PromptTemplate
from ...utils.logging import setup_logger

logger = setup_logger(__name__)


class OpenAIPromptTemplate(PromptTemplate):
    """OpenAI-specific prompt template implementation."""

    def __init__(self, template_path: Optional[Path] = None):
        super().__init__(template_path)
        self._load_default_template()

    def _load_default_template(self) -> None:
        """Load the default prompt template if no custom one provided."""
        self.template = """
        Generate a PyTorch neural network implementation based on the following architecture specification:
        {arch_spec}
        
        Requirements:
        - Use PyTorch nn.Module as the base class
        - Include all necessary imports
        - Implement __init__ and forward methods
        - Follow Python best practices and type hints
        - Ensure the implementation matches the spec exactly
        
        Return only the code, no explanations.
        """

    def build_prompt(self, arch_spec: Dict[str, Any]) -> str:
        """Convert architecture spec into a prompt string."""
        spec_str = "\n".join(f"- {k}: {v}" for k, v in arch_spec.items())
        return self.template.format(arch_spec=spec_str)

    def parse_response(self, response: str) -> str:
        """Extract clean Python code from the response."""
        # Remove any markdown code blocks if present
        code = response.strip()
        if code.startswith("```python"):
            code = code.split("```python", 1)[1]
        if code.startswith("```"):
            code = code.split("```", 1)[1]
        if code.endswith("```"):
            code = code.rsplit("```", 1)[0]
        return code.strip()


class OpenAICodeGenerator(CodeGenerator):
    """
    Code generator implementation using OpenAI's API.

    Attributes:
        client: AsyncOpenAI client instance
        model: Name of the OpenAI model to use
        temperature: Sampling temperature for generation
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the OpenAI code generator."""
        super().__init__(config)

        api_key = config.get("openai_api_key")
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set it in the config or OPENAI_API_KEY environment variable."
            )

        self.client = AsyncOpenAI(api_key=api_key)
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.7)

    def _setup_template(self) -> None:
        """Initialize the OpenAI-specific prompt template."""
        self.prompt_template = OpenAIPromptTemplate()

    async def generate_code(
        self, arch_spec: Dict[str, Any], max_retries: int = 3
    ) -> str:
        """Generate code using OpenAI's API."""
        prompt = self.prompt_template.build_prompt(arch_spec)

        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert PyTorch developer.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=self.temperature,
                )

                code = self.prompt_template.parse_response(
                    response.choices[0].message.content
                )

                if await self.validate_code(code):
                    return code

            except Exception as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise

        raise RuntimeError("Failed to generate valid code after max retries")

    async def validate_code(
        self, code: str, validation_tests: Optional[List[str]] = None
    ) -> bool:
        """Validate the generated code."""
        # Check syntax
        try:
            ast.parse(code)
        except SyntaxError:
            return False

        # Basic import validation
        if "import torch" not in code or "import torch.nn as nn" not in code:
            return False

        # Check for required class structure
        if (
            "class" not in code
            or "def __init__" not in code
            or "def forward" not in code
        ):
            return False

        # Run additional validation tests if provided
        if validation_tests:
            # TODO: Implement custom validation tests
            pass

        return True

    async def repair_code(self, code: str, error_message: str) -> str:
        """Attempt to fix invalid code using the API."""
        repair_prompt = f"""
        The following PyTorch code has an error:
        
        {code}
        
        Error message:
        {error_message}
        
        Please fix the code and return only the corrected version.
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert PyTorch developer.",
                    },
                    {"role": "user", "content": repair_prompt},
                ],
                temperature=self.temperature,
            )

            fixed_code = self.prompt_template.parse_response(
                response.choices[0].message.content
            )

            if await self.validate_code(fixed_code):
                return fixed_code

        except Exception as e:
            logger.error(f"Code repair failed: {str(e)}")
            raise

        raise RuntimeError("Failed to repair code")
