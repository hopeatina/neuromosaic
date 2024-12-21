---
title: "Adding New Architectures"
description: "Learn how to extend NeuroMosaic with new neural architecture types"
---

# Adding New Architectures

This guide explains how to add support for new neural architecture types in NeuroMosaic.

## Overview

Adding a new architecture type requires implementing:

1. Architecture specification
2. Encoder/decoder
3. Performance evaluator
4. Search space definition

## Architecture Specification

Create a new class inheriting from `BaseArchitecture`:

```python
from neuromosaic.architectures import BaseArchitecture
from typing import Dict, Any

class CustomArchitecture(BaseArchitecture):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config

    def to_model(self):
        """Convert specification to PyTorch model"""
        # Implementation here

    def to_dict(self) -> Dict[str, Any]:
        """Serialize architecture to dictionary"""
        return self.config

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'CustomArchitecture':
        """Create architecture from dictionary"""
        return cls(config)
```

## Encoder/Decoder

Implement encoding to continuous space:

```python
from neuromosaic.encoding import BaseEncoder

class CustomEncoder(BaseEncoder):
    def encode(self, architecture: CustomArchitecture) -> np.ndarray:
        """Convert architecture to vector representation"""
        # Implementation here

    def decode(self, vector: np.ndarray) -> CustomArchitecture:
        """Convert vector back to architecture"""
        # Implementation here
```

## Performance Evaluator

Create evaluation logic:

```python
from neuromosaic.evaluation import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def evaluate(self, architecture: CustomArchitecture) -> Dict[str, float]:
        """Evaluate architecture performance"""
        model = architecture.to_model()
        # Training/evaluation logic
        return {
            "accuracy": accuracy,
            "latency": latency,
            "params": param_count
        }
```

## Search Space Definition

Define the search space:

```python
from neuromosaic.search import SearchSpace

custom_space = SearchSpace(
    parameters={
        "num_layers": {"type": "int", "min": 1, "max": 50},
        "hidden_dim": {"type": "int", "min": 32, "max": 512},
        "activation": {"type": "categorical", "values": ["relu", "gelu"]}
    },
    constraints=[
        lambda x: x["num_layers"] * x["hidden_dim"] < 10000
    ]
)
```

## Registration

Register your components:

```python
from neuromosaic.registry import register_architecture

register_architecture(
    name="custom",
    architecture_class=CustomArchitecture,
    encoder_class=CustomEncoder,
    evaluator_class=CustomEvaluator,
    search_space=custom_space
)
```

## Testing

### Unit Tests

```python
def test_custom_architecture():
    config = {
        "num_layers": 10,
        "hidden_dim": 128,
        "activation": "relu"
    }

    # Test creation
    arch = CustomArchitecture(config)
    assert arch.to_dict() == config

    # Test encoding/decoding
    encoder = CustomEncoder()
    vector = encoder.encode(arch)
    decoded = encoder.decode(vector)
    assert decoded.to_dict() == config
```

### Integration Tests

```python
def test_search_integration():
    from neuromosaic.search import ArchitectureSearch

    search = ArchitectureSearch(
        architecture_type="custom",
        max_trials=10
    )
    results = search.run()
    assert len(results) == 10
```

## Best Practices

1. **Encoding Design**

   - Preserve architectural semantics
   - Ensure smooth interpolation
   - Handle invalid configurations

2. **Evaluation Efficiency**

   - Implement caching
   - Use hardware acceleration
   - Enable parallel evaluation

3. **Error Handling**
   - Validate configurations
   - Handle edge cases
   - Provide meaningful errors

## Example: ResNet Extension

Here's a complete example extending ResNet:

```python
class ResNetArchitecture(BaseArchitecture):
    def __init__(self, config):
        super().__init__()
        self.depth = config["depth"]
        self.width = config["width"]
        self.bottleneck = config["bottleneck"]

    def to_model(self):
        return ResNet(
            depth=self.depth,
            width=self.width,
            bottleneck=self.bottleneck
        )

class ResNetEncoder(BaseEncoder):
    def encode(self, arch):
        return np.array([
            arch.depth / 200,  # Normalize
            arch.width / 64,
            float(arch.bottleneck)
        ])

    def decode(self, vector):
        return ResNetArchitecture({
            "depth": int(vector[0] * 200),
            "width": int(vector[1] * 64),
            "bottleneck": bool(round(vector[2]))
        })

# Register
register_architecture(
    "resnet",
    ResNetArchitecture,
    ResNetEncoder,
    ResNetEvaluator,
    resnet_search_space
)
```

## Troubleshooting

<Accordion title="Encoding Issues">
- Check normalization
- Verify invertibility
- Test edge cases
</Accordion>

<Accordion title="Performance Problems">
- Profile evaluation code
- Check memory usage
- Optimize bottlenecks
</Accordion>

## Next Steps

- Learn about [LLM integration](/developer/llm-providers)
- Explore [FastAPI endpoints](/developer/fastapi-integration)
- Study [example architectures](/research/experiment-case-studies)
