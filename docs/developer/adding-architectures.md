---
title: "Adding New Architectures"
description: "Learn how to extend Neuromosaic with new neural architecture types"
---

<Note>
  This guide is for developers who want to extend Neuromosaic's capabilities by adding support for new neural architecture types. Make sure you're familiar with the [platform overview](/platform/overview) before proceeding.
</Note>

## Implementation Checklist

<Steps>
  1. Create an **Architecture Specification** class
  2. Implement the **Encoder/Decoder** for continuous space representation
  3. Build a **Performance Evaluator** for your architecture
  4. Define the **Search Space** parameters
  5. **Register** your components with Neuromosaic
</Steps>

## Architecture Specification

<CodeGroup>
```python Base Class
from neuromosaic.architectures import BaseArchitecture
from typing import Dict, Any

class CustomArchitecture(BaseArchitecture):
def **init**(self, config: Dict[str, Any]):
super().**init**()
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

````

```python ResNet Example
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
````

</CodeGroup>

## Encoder/Decoder Implementation

<Info>
  The encoder/decoder is crucial for mapping architectures to and from a continuous space where meta-learning can occur.
</Info>

<CodeGroup>
```python Base Encoder
from neuromosaic.encoding import BaseEncoder

class CustomEncoder(BaseEncoder):
def encode(self, architecture: CustomArchitecture) -> np.ndarray:
"""Convert architecture to vector representation""" # Implementation here

    def decode(self, vector: np.ndarray) -> CustomArchitecture:
        """Convert vector back to architecture"""
        # Implementation here

````

```python ResNet Encoder
class ResNetEncoder(BaseEncoder):
    def encode(self, arch):
        return np.array([
            arch.depth / 200,  # Normalize to [0,1]
            arch.width / 64,
            float(arch.bottleneck)
        ])

    def decode(self, vector):
        return ResNetArchitecture({
            "depth": int(vector[0] * 200),
            "width": int(vector[1] * 64),
            "bottleneck": bool(round(vector[2]))
        })
````

</CodeGroup>

## Performance Evaluator

<Warning>
  Ensure your evaluator handles edge cases and provides meaningful error messages when architectures fail to train or evaluate.
</Warning>

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

<Accordion title="Search Space Parameters">
Define the valid ranges and constraints for your architecture:

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

</Accordion>

## Component Registration

<CodeGroup>
```python Basic Registration
from neuromosaic.registry import register_architecture

register_architecture(
name="custom",
architecture_class=CustomArchitecture,
encoder_class=CustomEncoder,
evaluator_class=CustomEvaluator,
search_space=custom_space
)

````

```python With Options
register_architecture(
    name="custom",
    architecture_class=CustomArchitecture,
    encoder_class=CustomEncoder,
    evaluator_class=CustomEvaluator,
    search_space=custom_space,
    options={
        "cache_evaluations": True,
        "parallel_evaluation": True,
        "max_retries": 3
    }
)
````

</CodeGroup>

## Testing Your Implementation

<Tabs>
  <Tab title="Unit Tests">
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

  </Tab>
  <Tab title="Integration Tests">
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

  </Tab>
</Tabs>

## Best Practices

<CardGroup cols={2}>
  <Card title="Encoding Design" icon="code">
    - Preserve architectural semantics
    - Ensure smooth interpolation
    - Handle invalid configurations
  </Card>
  <Card title="Evaluation Efficiency" icon="gauge">
    - Implement caching
    - Use hardware acceleration
    - Enable parallel evaluation
  </Card>
  <Card title="Error Handling" icon="triangle-exclamation">
    - Validate configurations
    - Handle edge cases
    - Provide meaningful errors
  </Card>
  <Card title="Testing" icon="vial">
    - Write comprehensive tests
    - Cover edge cases
    - Test performance at scale
  </Card>
</CardGroup>

## Troubleshooting

<Accordion title="Common Encoding Issues">
  - Check normalization ranges
  - Verify encoder/decoder invertibility
  - Test edge cases and invalid inputs
  - Monitor numerical stability
</Accordion>

<Accordion title="Performance Problems">
  - Profile evaluation code
  - Check memory usage patterns
  - Optimize computational bottlenecks
  - Consider batch processing
</Accordion>

<Accordion title="Integration Issues">
  - Verify component registration
  - Check API compatibility
  - Monitor resource usage
  - Test concurrent operations
</Accordion>

## Next Steps

<Check>
  Now that you've added a new architecture type, you can:
  - [Integrate with LLM providers](/developer/llm-providers)
  - [Add FastAPI endpoints](/developer/fastapi-integration)
  - [Study example architectures](/research/experiment-case-studies)
</Check>
