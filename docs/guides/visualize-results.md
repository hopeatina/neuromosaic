---
title: "Visualizing Results"
description: "Learn how to use and interpret NeuroMosaic's interactive visualizations"
---

# Visualizing Results

NeuroMosaic provides powerful interactive visualizations to help you understand and explore the architecture search space. This guide explains how to use each visualization type and interpret the results.

## 3D Scatter Plot

The primary visualization is an interactive 3D scatter plot where each point represents a neural architecture.

### Basic Navigation

- **Rotate**: Click and drag
- **Zoom**: Scroll wheel
- **Pan**: Right-click and drag
- **Reset View**: Double-click

### Interactive Features

<CodeGroup>
```python Hover Information
# Example hover data format
{
    "Architecture": "ResNet-18",
    "Accuracy": "94.2%",
    "Parameters": "11.7M",
    "Training Time": "2.3 hours"
}
```

```python Point Selection
# Select points by:
- Click individual points
- Box select (Shift + click + drag)
- Lasso select (Alt + click + drag)
```

</CodeGroup>

### Color Mapping

Points are colored based on performance metrics:

- **Blue → Red**: Low to high performance
- **Opacity**: Confidence/uncertainty
- **Size**: Can represent secondary metrics

## Timeline Plot

The timeline plot shows how metrics evolve during the search process.

### Features

1. **Multiple Metrics**

   - Toggle different metrics on/off
   - Compare trends across metrics
   - Hover for exact values

2. **Time Windows**
   - Zoom to specific time ranges
   - Pan through history
   - Reset to full view

## Parallel Coordinates

This plot helps visualize relationships between different architecture parameters and performance metrics.

### Usage Tips

1. **Parameter Ranges**

   - Drag along axes to filter ranges
   - Double-click axis to reset
   - Reorder axes by dragging labels

2. **Pattern Analysis**
   - Look for parallel lines (correlated parameters)
   - Identify bottlenecks
   - Find high-performing regions

## Example Workflows

### Finding Optimal Architectures

1. Start with the 3D scatter plot
2. Identify high-performing clusters
3. Use parallel coordinates to understand parameters
4. Check timeline for convergence

```python
# Example code for extracting top architectures
top_architectures = filter_points(
    metric_threshold=0.95,  # Top 5%
    cluster_size_min=5      # Stable regions
)
```

### Comparing Architecture Families

1. Use color coding for architecture types
2. Analyze clustering patterns
3. Compare performance distributions
4. Identify hybrid opportunities

## Customization Options

### Plot Settings

```python
# Example configuration
plot_config = {
    "colormap": "viridis",
    "point_size": 8,
    "opacity": 0.8,
    "axis_labels": True
}
```

### Data Filters

- Filter by metric ranges
- Show/hide architecture families
- Highlight selected points
- Focus on time windows

## Exporting Results

### Available Formats

1. **Static Images**

   - PNG for presentations
   - SVG for publications
   - High-resolution options

2. **Interactive HTML**

   - Standalone files
   - Embed in documents
   - Share with colleagues

3. **Data Export**
   - CSV for further analysis
   - JSON for programmatic use
   - Architecture specifications

## Best Practices

1. **Start Broad**

   - View full search space first
   - Identify interesting regions
   - Gradually zoom in

2. **Use Multiple Views**

   - Combine different plot types
   - Cross-reference findings
   - Validate patterns

3. **Document Insights**
   - Save important views
   - Note significant patterns
   - Track search progress

## Troubleshooting

<Accordion title="Visualization Performance">
- Reduce point count for smoother interaction
- Use simpler color schemes
- Enable hardware acceleration
</Accordion>

<Accordion title="Data Updates">
- Check WebSocket connection
- Verify data pipeline
- Clear browser cache
</Accordion>

## Next Steps

- Learn about [running experiments](/guides/run-experiments)
- Understand [meta-learning](/research/meta-learning-insights)
- Explore [architecture space](/research/sphere-metaphor)
