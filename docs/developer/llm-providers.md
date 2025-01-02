---
title: "LLM Provider Integration"
description: "Learn how to integrate new language model providers for architecture generation and optimization"
---

# LLM Provider Integration

This guide explains how to integrate new language model providers for neural architecture generation and optimization.

## Overview

Neuromosaic uses language models to:

1. Generate architecture descriptions
2. Parse natural language constraints
3. Optimize architecture configurations
4. Explain search decisions

## Provider Interface

Create a new provider by implementing the `BaseLLMProvider`:

```python
from neuromosaic.llm import BaseLLMProvider
from typing import Dict, Any, List

class CustomLLMProvider(BaseLLMProvider):
    def __init__(self, api_key: str, **kwargs):
        super().__init__()
        self.api_key = api_key
        self.config = kwargs

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 100
    ) -> str:
        """Generate text completion"""
        # Implementation here

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str:
        """Chat completion interface"""
        # Implementation here
```

## Authentication

Handle API keys securely:

```python
from neuromosaic.config import Settings
from neuromosaic.security import encrypt_key

class CustomLLMAuth:
    @staticmethod
    def setup_auth(api_key: str) -> None:
        """Store encrypted API key"""
        encrypted = encrypt_key(api_key)
        Settings.update({
            "custom_llm_key": encrypted
        })

    @staticmethod
    def get_credentials() -> Dict[str, str]:
        """Retrieve and decrypt key"""
        return {
            "api_key": Settings.decrypt_key("custom_llm_key")
        }
```

## Prompt Templates

Define templates for different tasks:

```python
from neuromosaic.prompts import PromptTemplate

architecture_prompt = PromptTemplate(
    """Design a neural network architecture that:
    - Satisfies: {constraints}
    - Optimizes for: {objectives}
    - Uses components: {components}

    Respond with a valid architecture configuration."""
)

optimization_prompt = PromptTemplate(
    """Suggest improvements to the architecture:
    {current_config}

    Based on these metrics:
    {performance_metrics}

    Maintain these constraints:
    {constraints}"""
)
```

## Response Parsing

Implement response parsing:

```python
from neuromosaic.parsing import BaseParser

class CustomResponseParser(BaseParser):
    def parse_architecture(self, response: str) -> Dict[str, Any]:
        """Parse architecture description"""
        # Implementation here

    def parse_optimization(self, response: str) -> List[Dict[str, Any]]:
        """Parse optimization suggestions"""
        # Implementation here
```

## Integration Example

Here's how to use the custom provider:

```python
from neuromosaic.llm import LLMManager

# Register provider
LLMManager.register_provider("custom", CustomLLMProvider)

# Initialize
llm = LLMManager.get_provider(
    "custom",
    api_key="your-api-key",
    model="custom-model"
)

# Generate architecture
config = await llm.generate_architecture(
    constraints=["max_params=10M", "min_accuracy=0.95"],
    objectives=["accuracy", "latency"],
    components=["convolution", "attention"]
)

# Optimize existing
improvements = await llm.optimize_architecture(
    current_config=config,
    metrics={"accuracy": 0.93, "latency": 15.2},
    constraints=["max_params=10M"]
)
```

## Caching and Rate Limiting

Implement efficient API usage:

```python
from neuromosaic.caching import Cache
from neuromosaic.rate_limiting import RateLimiter

class CachedLLMProvider(CustomLLMProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = Cache()
        self.rate_limiter = RateLimiter(
            calls_per_minute=60,
            burst_limit=10
        )

    async def generate(self, *args, **kwargs):
        # Check cache
        cache_key = self.cache.compute_key(args, kwargs)
        if cached := self.cache.get(cache_key):
            return cached

        # Rate limit
        await self.rate_limiter.acquire()

        # Generate and cache
        result = await super().generate(*args, **kwargs)
        self.cache.set(cache_key, result)
        return result
```

## Error Handling

Handle API-specific errors:

```python
from neuromosaic.exceptions import LLMError

class CustomLLMError(LLMError):
    """Custom provider-specific errors"""
    pass

def handle_api_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ApiError as e:
            raise CustomLLMError(f"API error: {str(e)}")
        except RateLimitError:
            raise CustomLLMError("Rate limit exceeded")
    return wrapper
```

## Testing

### Unit Tests

```python
async def test_custom_provider():
    provider = CustomLLMProvider(api_key="test")

    # Test generation
    response = await provider.generate(
        "Design a CNN for image classification"
    )
    assert isinstance(response, str)

    # Test parsing
    parser = CustomResponseParser()
    config = parser.parse_architecture(response)
    assert "layers" in config
```

### Integration Tests

```python
async def test_end_to_end():
    llm = LLMManager.get_provider("custom")

    # Test architecture generation
    config = await llm.generate_architecture(
        constraints=["max_params=10M"]
    )

    # Test optimization
    improvements = await llm.optimize_architecture(
        current_config=config,
        metrics={"accuracy": 0.9}
    )
```

## Best Practices

1. **Prompt Engineering**

   - Use clear, structured prompts
   - Include examples in templates
   - Handle edge cases

2. **Error Recovery**

   - Implement retries
   - Fallback options
   - Clear error messages

3. **Resource Management**
   - Efficient token usage
   - Response caching
   - Connection pooling

## Troubleshooting

<Accordion title="API Issues">
- Check API key validity
- Verify endpoint URLs
- Monitor rate limits
</Accordion>

<Accordion title="Parsing Errors">
- Validate response format
- Check for schema changes
- Handle malformed responses
</Accordion>

## Next Steps

- Explore [FastAPI integration](/developer/fastapi-integration)
- Learn about [architecture types](/developer/adding-architectures)
- Study [meta-learning](/research/meta-learning-insights)
