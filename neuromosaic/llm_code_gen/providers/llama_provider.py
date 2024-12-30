"""
LLaMA-based code generator implementation supporting both local and cloud deployments.

For local deployment:
- Uses llama-cpp-python library to run LLaMA models locally
- Supports both CPU and GPU inference
- Works with various LLaMA model formats including GGUF (recommended)

For cloud deployment:
- Uses DeepSeek's OpenAI-compatible API
- Requires only an API key
- Compatible with OpenAI SDK

For GPU support in local deployment, llama-cpp-python must be installed with CUDA support:
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
"""

import ast
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from llama_cpp import Llama
from openai import OpenAI

from ..codegen_interface import CodeGenerator, PromptTemplate
from ...utils.logging import setup_logger

logger = setup_logger(__name__)


class MockCodeGenerator(CodeGenerator):
    """
    Mock code generator for development and testing.
    Returns predefined responses without making actual LLM calls.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the mock code generator."""
        super().__init__(config)
        self._setup_template()
        logger.info("Initialized MockCodeGenerator for development/testing")

    def _setup_template(self) -> None:
        """No template needed for mock generator."""
        pass

    async def generate_code(
        self, arch_spec: Dict[str, Any], max_retries: int = 3
    ) -> str:
        """Return a mock PyTorch implementation."""
        logger.info("MockCodeGenerator.generate_code called with spec: %s", arch_spec)
        return """
import torch
import torch.nn as nn

class MockNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv(x)
        x = self.relu(x)
        x = self.pool(x)
        return x
        """

    async def validate_code(
        self, code: str, validation_tests: Optional[List[str]] = None
    ) -> bool:
        """Always return True for mock validation."""
        return True

    async def repair_code(self, code: str, error_message: str) -> str:
        """Return the same code for mock repair."""
        return code


class LlamaPromptTemplate(PromptTemplate):
    """LLaMA-specific prompt template implementation."""

    def __init__(self, template_path: Optional[Path] = None):
        super().__init__(template_path)
        self._load_default_template()

    def _load_default_template(self) -> None:
        """Load the default prompt template if no custom one provided."""
        self.template = """You are an expert PyTorch developer. Your task is to generate a PyTorch neural network implementation based on the following architecture specification:

{arch_spec}

Requirements:
- Use PyTorch nn.Module as the base class
- Include all necessary imports
- Implement __init__ and forward methods
- Follow Python best practices and type hints
- Ensure the implementation matches the spec exactly

Return only the code, no explanations. Start with imports and then the class definition."""

    def build_prompt(self, arch_spec: Dict[str, Any]) -> str:
        """Convert architecture spec into a prompt string."""
        spec_str = "\n".join(f"- {k}: {v}" for k, v in arch_spec.items())
        return self.template.format(arch_spec=spec_str)

    def parse_response(self, response: str) -> str:
        """Extract clean Python code from the response."""
        code = response.strip()
        # Remove any code block formatting
        if code.startswith("```python"):
            code = code.split("```python", 1)[1]
        if code.startswith("```"):
            code = code.split("```", 1)[1]
        if code.endswith("```"):
            code = code.rsplit("```", 1)[0]
        return code.strip()


class LlamaCodeGenerator(CodeGenerator):
    """
    Code generator implementation supporting both local and cloud-hosted LLaMA models.

    This implementation supports:
    - Local deployment with CPU/GPU inference
    - Cloud deployment using DeepSeek's OpenAI-compatible API
    - Configurable parameters for both deployment types
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the LLaMA code generator.

        Args:
            config: Configuration dictionary containing:
                Common fields:
                - deployment_type: "local" or "cloud"
                - temperature: Sampling temperature (default: 0.7)
                - max_tokens: Maximum tokens to generate (default: 2048)
                - top_p: Top-p sampling parameter (default: 0.95)

                For local deployment:
                - model_path: Path to the model file
                - n_ctx: Context window size (default: 2048)
                - n_gpu_layers: Number of layers to offload to GPU (default: 0)
                - n_batch: Batch size for prompt processing (default: 512)

                For cloud deployment:
                - deepseek_api_key: API key for DeepSeek service
                - api_base: Base URL for API endpoint (optional)
                - model: Model to use (default: deepseek-chat)
        """
        super().__init__(config)

        self.deployment_type = config.get("deployment_type", "local")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2048)
        self.top_p = config.get("top_p", 0.95)

        if self.deployment_type == "local":
            model_path = config.get("model_path")
            if not model_path:
                raise ValueError("LLaMA model path is required for local deployment")

            # Initialize local model
            self.model = Llama(
                model_path=model_path,
                n_ctx=config.get("n_ctx", 2048),
                n_gpu_layers=config.get("n_gpu_layers", 0),
                n_batch=config.get("n_batch", 512),
            )
            logger.info(
                "Initialized local LlamaCodeGenerator with model: %s, temp: %f",
                model_path,
                self.temperature,
            )
        else:  # cloud deployment
            api_key = config.get("deepseek_api_key")
            if not api_key:
                raise ValueError("DeepSeek API key is required for cloud deployment")

            # Initialize OpenAI client with DeepSeek configuration
            self.client = OpenAI(
                api_key=api_key,
                base_url=config.get("api_base", "https://api.deepseek.com/v1"),
            )
            self.model_name = config.get("model", "deepseek-chat")
            logger.info(
                "Initialized cloud LlamaCodeGenerator with model: %s",
                self.model_name,
            )

    def _setup_template(self) -> None:
        """Initialize the LLaMA-specific prompt template."""
        self.prompt_template = LlamaPromptTemplate()

    async def generate_code(
        self, arch_spec: Dict[str, Any], max_retries: int = 3
    ) -> str:
        """Generate code using either local or cloud LLaMA model.

        Args:
            arch_spec: Architecture specification dictionary
            max_retries: Maximum number of generation attempts

        Returns:
            str: Generated PyTorch code

        Raises:
            RuntimeError: If generation fails after max retries
        """
        prompt = self.prompt_template.build_prompt(arch_spec)

        for attempt in range(max_retries):
            try:
                if self.deployment_type == "local":
                    response = self.model.create_completion(
                        prompt,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        top_p=self.top_p,
                        stop=["```"],
                    )
                    code = self.prompt_template.parse_response(
                        response["choices"][0]["text"]
                    )
                else:  # cloud deployment
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an expert PyTorch developer.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        top_p=self.top_p,
                        stop=["```"],
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
        """Validate the generated code.

        Args:
            code: Generated code to validate
            validation_tests: Optional list of additional test cases

        Returns:
            bool: True if code passes validation
        """
        # Check syntax
        try:
            ast.parse(code)
        except SyntaxError:
            logger.warning("Generated code has syntax errors")
            return False

        # Basic import validation
        if "import torch" not in code or "import torch.nn as nn" not in code:
            logger.warning("Generated code missing required imports")
            return False

        # Check for required class structure
        if "class" not in code:
            logger.warning("Generated code missing class definition")
            return False
        if "def __init__" not in code:
            logger.warning("Generated code missing __init__ method")
            return False
        if "def forward" not in code:
            logger.warning("Generated code missing forward method")
            return False

        # Run additional validation tests if provided
        if validation_tests:
            for test in validation_tests:
                try:
                    exec(test)
                except Exception as e:
                    logger.warning(f"Validation test failed: {str(e)}")
                    return False

        return True

    async def repair_code(self, code: str, error_message: str) -> str:
        """Attempt to fix invalid code using the model.

        Args:
            code: The code to fix
            error_message: The error message to address

        Returns:
            str: Fixed code

        Raises:
            RuntimeError: If repair fails
        """
        repair_prompt = f"""Fix the following PyTorch code that has an error:

Error message:
{error_message}

Code to fix:
```python
{code}
```

Return only the fixed code, no explanations."""

        try:
            response = self.model.create_completion(
                repair_prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                stop=["```"],
            )

            fixed_code = self.prompt_template.parse_response(
                response["choices"][0]["text"]
            )

            if await self.validate_code(fixed_code):
                return fixed_code

        except Exception as e:
            logger.error(f"Code repair failed: {str(e)}")
            raise

        raise RuntimeError("Failed to repair code")
