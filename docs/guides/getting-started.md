---
title: "Getting Started"
description: "Set up NeuroMosaic and run your first architecture exploration"
---

# Getting Started with NeuroMosaic

This guide will walk you through setting up NeuroMosaic and running your first architecture exploration experiment.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/neuromosaic.git
cd neuromosaic
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Launch the Dashboard

1. Start the FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

2. In a new terminal, launch the frontend:

```bash
cd frontend
streamlit run app.py
```

The dashboard should now be accessible at `http://localhost:8501`.

## Your First Experiment

1. **Configure Search Space**

   - Navigate to the "Configuration" tab
   - Select your target architecture type
   - Define parameter ranges for exploration

2. **Launch Exploration**

   - Click "Start Exploration" to begin the search
   - Watch as points appear in the 3D visualization
   - Monitor metrics in real-time

3. **Analyze Results**
   - Use the 3D scatter plot to identify promising regions
   - Check the timeline plot for convergence
   - Export results for further analysis

## Understanding the Visualization

The main 3D scatter plot shows:

- Each point = One architecture configuration
- Color = Performance metric
- Clustering = Similar architectures
- Hover for detailed information

## Next Steps

- Learn about [architecture representation](/research/sphere-metaphor)
- Explore [visualization features](/guides/visualize-results)
- Understand how to [interpret results](/guides/interpret-outcomes)
- Set up [custom experiments](/guides/run-experiments)

## Troubleshooting

Common issues and solutions:

<Accordion title="Dashboard not loading">
  - Check if both backend and frontend servers are running
  - Verify ports 8000 (API) and 8501 (Dashboard) are available
  - Check console for error messages
</Accordion>

<Accordion title="Visualization not updating">
  - Ensure WebSocket connection is active
  - Try refreshing the browser
  - Check backend logs for errors
</Accordion>

## Need Help?

- Check our [GitHub Issues](https://github.com/yourusername/neuromosaic/issues)
- Review the [Developer Guide](/developer/adding-architectures)
- Join our community discussions
