---
title: "Running Experiments"
description: "Learn how to configure and run architecture search experiments"
---

<Note>
  This guide explains how to configure and run architecture search experiments in Neuromosaic.
  Some advanced features described here are planned for future releases.
  
  View the full documentation at [https://neuromosaic.mintlify.app/](https://neuromosaic.mintlify.app/)
</Note>

## Quick Start

The fastest way to start is using the `quickstart` command:

```bash
# Basic architecture search
python -m neuromosaic quickstart

# With GPU and parallel execution
python -m neuromosaic quickstart --gpu --batch-size 8

# Customize output directory and use CPU
python -m neuromosaic quickstart --output-dir my_search --cpu --batch-size 4
```

## Custom Experiments

For more control over the search process:

1. Create a custom configuration file (e.g., `custom_config.yaml`):

```yaml
# Example configuration
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

## Available Commands

<CardGroup cols={2}>
  <Card title="Quickstart" icon="play">
    Available Now:
    - Basic architecture search
    - GPU/CPU selection
    - Parallel execution
    - Output directory selection
  </Card>
  
  <Card title="Custom Experiments" icon="sliders">
    Available Now:
    - Custom configuration
    - Sequential/parallel execution
    - Resume capability
    - Basic metrics tracking
  </Card>
  
  <Card title="Analysis (Coming Soon)" icon="chart-line">
    - Compare experiments
    - Generate reports
    - Export results
    - Visualize search space
  </Card>
  
  <Card title="Advanced Features (Coming Soon)" icon="wand-magic-sparkles">
    - Meta-learning optimization
    - Distributed training
    - Custom search strategies
    - Advanced metrics
  </Card>
</CardGroup>

## Monitoring Progress

<Tabs>
  <Tab title="Basic Monitoring">
    Available Now:
    ```bash
    # View experiment logs
    tail -f neuromosaic.log

    # Check experiment status
    python -m neuromosaic experiment --config config.yaml --status
    ```

  </Tab>
  
  <Tab title="Advanced Monitoring (Coming Soon)">
    ```python
    # Real-time monitoring dashboard
    python -m neuromosaic dashboard
    
    # Access at http://localhost:8050
    ```
  </Tab>
</Tabs>

## Configuration Options

<Accordion title="Basic Settings">
Available Now:
- Experiment name
- Search space definition
- Number of trials
- Resource limits
</Accordion>

<Accordion title="Advanced Settings (Coming Soon)">
- Custom search strategies
- Distributed resources
- Meta-learning parameters
- Advanced metrics
</Accordion>

## Best Practices

<Warning>
  Start with the quickstart command to verify your setup before moving to custom experiments.
</Warning>

<Steps>
  1. **Initial Setup**
     - Use quickstart command
     - Verify basic functionality
     - Check resource availability

2.  **Custom Configuration**

    - Start with minimal changes
    - Test configuration validity
    - Monitor resource usage

3.  **Scaling Up**
    Available Now: - Increase batch size - Adjust resource limits
    Coming Soon: - Distributed execution - Advanced optimization
    </Steps>

## Troubleshooting

<Accordion title="Common Issues">
  - Check if API server is running
  - Verify port availability
  - Review error messages in logs
  - Check configuration syntax
</Accordion>

<Accordion title="Resource Issues">
  - Monitor CPU/GPU usage
  - Check memory availability
  - Verify disk space
  - Review network connectivity
</Accordion>

## Next Steps

<Check>
  Ready to analyze your results?
  
  Available Now:
  - Basic experiment configuration
  - Simple metrics tracking
  
  Coming Soon:
  - [Advanced visualization](https://neuromosaic.mintlify.app/guides/visualize-results)
  - [Result interpretation](https://neuromosaic.mintlify.app/guides/interpret-outcomes)
  - [Meta-learning insights](https://neuromosaic.mintlify.app/research/meta-learning-insights)
  
  Note: Some features mentioned in the documentation are still under development.
</Check>

<Info>
  Need help? Join our [Discord community](https://discord.gg/neuromosaic) or check our [GitHub Issues](https://github.com/neuromosaic/neuromosaic/issues).
  
  Full documentation: [https://neuromosaic.mintlify.app/](https://neuromosaic.mintlify.app/)
</Info>
