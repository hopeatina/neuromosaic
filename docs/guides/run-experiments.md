---
title: "Running Experiments"
description: "Learn how to configure and run architecture search experiments"
---

# Running Experiments

This guide explains how to configure and run architecture search experiments in NeuroMosaic.

## Experiment Configuration

### Basic Settings

```python
experiment_config = {
    "name": "resnet_search",
    "search_space": "resnet",
    "max_trials": 100,
    "optimization_metric": "accuracy"
}
```

### Search Space Definition

1. **Architecture Type**

   - Choose base architecture family
   - Define parameter ranges
   - Set constraints

2. **Optimization Goals**
   - Primary metric (e.g., accuracy)
   - Secondary objectives (e.g., latency)
   - Constraints (e.g., model size)

## Running the Search

### Through the Dashboard

1. Navigate to "New Experiment"
2. Fill in configuration form
3. Click "Start Search"
4. Monitor progress in real-time

### Via API

```python
from neuromosaic.client import NeuroMosaicClient

client = NeuroMosaicClient()
experiment = client.create_experiment(experiment_config)
experiment.start()
```

## Monitoring Progress

### Key Metrics

- Best architecture found
- Search efficiency
- Resource utilization
- Convergence indicators

### Real-time Updates

1. **Dashboard Views**

   - 3D visualization of search progress
   - Performance timeline
   - Resource monitoring

2. **Logging**
   - Detailed logs in `experiments/logs/`
   - Metric history
   - Search decisions

## Search Strategies

### Random Search

```python
strategy_config = {
    "type": "random",
    "num_samples": 100
}
```

### Bayesian Optimization

```python
strategy_config = {
    "type": "bayesian",
    "acquisition_function": "expected_improvement",
    "kernel": "matern"
}
```

### Meta-Learning

```python
strategy_config = {
    "type": "meta",
    "prior_experiments": ["exp1", "exp2"],
    "adaptation_rate": 0.1
}
```

## Experiment Management

### Saving Results

1. **Automatic Saving**

   - Best architectures
   - Performance history
   - Search trajectory

2. **Manual Export**
   - CSV/JSON formats
   - Architecture configs
   - Visualization states

### Resuming Experiments

```python
# Resume from checkpoint
experiment.resume(
    checkpoint_path="experiments/checkpoints/exp_001/"
)
```

## Best Practices

1. **Start Small**

   - Begin with limited search space
   - Validate setup with quick runs
   - Gradually increase complexity

2. **Resource Management**

   - Monitor GPU utilization
   - Use appropriate batch sizes
   - Enable early stopping

3. **Reproducibility**
   - Set random seeds
   - Version control configs
   - Document environment

## Troubleshooting

<Accordion title="Search Not Converging">
- Check metric definitions
- Verify search space bounds
- Adjust optimization parameters
</Accordion>

<Accordion title="Resource Issues">
- Reduce parallel trials
- Optimize evaluation pipeline
- Check memory usage
</Accordion>

## Next Steps

- Learn to [interpret results](/guides/interpret-outcomes)
- Understand [meta-learning](/research/meta-learning-insights)
- Explore [case studies](/research/experiment-case-studies)
