# Frontend Development Guide

This guide covers the development and customization of the Neuromosaic dashboard interface.

## Architecture Overview

The frontend is organized into a modular structure:

```
neuromosaic/frontend/
├── __init__.py          # Package initialization
├── dashboard.py         # Main Dash application setup
├── utils.py            # Shared utilities and helpers
└── components/         # Dashboard UI components
    ├── __init__.py     # Components package
    ├── layout.py       # Dashboard layout structure
    ├── callbacks.py    # Interactive behavior handlers
    └── plots.py        # Visualization utilities
```

## Core Components

### Dashboard Application (`dashboard.py`)

The main entry point that initializes the Dash application. It:

- Sets up the application with appropriate themes and settings
- Integrates the layout and callbacks
- Provides server configuration

### Layout (`components/layout.py`)

Defines the dashboard's visual structure using Bootstrap components:

- Sidebar with controls and filters
- Main visualization area
- Detail panels for architecture information

### Callbacks (`components/callbacks.py`)

Handles all interactive behaviors:

- Updates to the 3D visualization
- Architecture detail display
- Experiment launching
- Metric filtering

### Plots (`components/plots.py`)

Provides visualization utilities:

- 3D scatter plots for architecture space
- Timeline plots for metric evolution
- Parallel coordinates for parameter relationships

### Utilities (`utils.py`)

Shared helper functions for:

- Data formatting
- API communication
- ResultsDB integration

## Development Workflow

1. **Setup Development Environment**

   ```bash
   # Install development dependencies
   pip install -r requirements-dev.txt

   # Start the dashboard in debug mode
   python -m neuromosaic dashboard --debug
   ```

2. **Making Changes**

   - Layout changes: Modify `components/layout.py`
   - New interactions: Add callbacks in `components/callbacks.py`
   - New visualizations: Add plot functions in `components/plots.py`
   - Data handling: Update utilities in `utils.py`

3. **Testing**

   ```bash
   # Run the test suite
   pytest tests/frontend/

   # Test specific components
   pytest tests/frontend/test_callbacks.py
   ```

## Adding New Features

### New Visualization Type

1. Add the plot function to `plots.py`:

   ```python
   def create_new_plot(data: Dict[str, Any]) -> go.Figure:
       """Create a new type of visualization.

       Args:
           data: The data to visualize

       Returns:
           A Plotly figure object
       """
       fig = go.Figure()
       # Add traces and layout
       return fig
   ```

2. Add to layout in `layout.py`:

   ```python
   dcc.Graph(
       id="new-plot-id",
       figure=create_new_plot({}),
       config={"displayModeBar": True}
   )
   ```

3. Add callback in `callbacks.py`:
   ```python
   @app.callback(
       Output("new-plot-id", "figure"),
       [Input("some-control", "value")]
   )
   def update_new_plot(value):
       # Update logic
       return create_new_plot(data)
   ```

### New Control Component

1. Add to sidebar in `layout.py`:

   ```python
   html.Div([
       html.H5("New Control"),
       dcc.Dropdown(
           id="new-control-id",
           options=[...],
           value=default_value
       )
   ])
   ```

2. Add callback handler in `callbacks.py`

### New Data Integration

1. Add utility functions in `utils.py`:

   ```python
   def process_new_data_type(data: Any) -> Dict[str, Any]:
       """Process new type of data for visualization."""
       # Processing logic
       return processed_data
   ```

2. Update relevant callbacks to use new data

## Best Practices

1. **Documentation**

   - Add detailed docstrings to all functions
   - Include type hints
   - Document complex callbacks

2. **Code Organization**

   - Keep components modular and focused
   - Use consistent naming conventions
   - Follow the established project structure

3. **Performance**

   - Minimize callback complexity
   - Cache expensive computations
   - Use efficient data structures

4. **Testing**
   - Write tests for new components
   - Test edge cases and error conditions
   - Verify callback behavior

## Common Tasks

### Adding a New Metric

1. Update `utils.py`:

   ```python
   def get_available_metrics():
       return [
           # Add new metric
           {"label": "New Metric", "value": "new_metric"}
       ]
   ```

2. Update relevant callbacks to handle the new metric

### Customizing the Theme

1. Modify Bootstrap theme in `dashboard.py`:

   ```python
   app = dash.Dash(
       __name__,
       external_stylesheets=[dbc.themes.CUSTOM_THEME]
   )
   ```

2. Add custom CSS in `assets/custom.css`

## Troubleshooting

Common issues and solutions:

1. **Callback Exceptions**

   - Check Input/Output dependencies
   - Verify data types match expectations
   - Add PreventUpdate where appropriate

2. **Performance Issues**

   - Profile callback execution time
   - Optimize data processing
   - Consider caching strategies

3. **Layout Problems**
   - Check Bootstrap grid usage
   - Verify responsive design
   - Test different screen sizes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

For more details, see the main [Contributing Guide](../CONTRIBUTING.md).
