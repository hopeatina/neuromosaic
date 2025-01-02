---
title: "Getting Started"
description: "Set up NeuroMosaic and run your first architecture exploration"
---

<Note>
  Welcome to NeuroMosaic! This guide will help you set up the platform and run your first neural architecture exploration experiment.
</Note>

## Quick Setup

<Steps>
  1. **Clone the Repository**
     ```bash
     git clone https://github.com/neuromosaic/neuromosaic.git
     cd neuromosaic
     ```

2. **Create Environment**
   <CodeGroup>

   ```bash macOS/Linux
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   ```bash Windows
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

   </CodeGroup>

3. **Launch Services**
   <Tabs>
   <Tab title="Backend">
   `bash
      uvicorn backend.main:app --reload
      `
   </Tab>
   <Tab title="Frontend">
   `bash
      cd frontend
      streamlit run app.py
      `
   </Tab>
   </Tabs>
   </Steps>

## Your First Experiment

<CardGroup cols={2}>
  <Card title="Configure Search" icon="sliders">
    Navigate to the "Configuration" tab and set up your exploration parameters:
    - Select architecture type
    - Define parameter ranges
    - Set optimization goals
  </Card>
  
  <Card title="Launch Search" icon="play">
    Start your architecture exploration:
    - Click "Start Exploration"
    - Monitor real-time progress
    - View emerging patterns
  </Card>
  
  <Card title="Analyze Results" icon="chart-line">
    Interpret your findings:
    - Use 3D visualization
    - Compare architectures
    - Export discoveries
  </Card>
  
  <Card title="Iterate & Refine" icon="rotate">
    Improve your results:
    - Adjust parameters
    - Focus on promising regions
    - Test hypotheses
  </Card>
</CardGroup>

## Understanding the Interface

<Accordion title="3D Visualization">
  The main scatter plot shows:
  - Each point represents an architecture
  - Colors indicate performance metrics
  - Clusters show similar designs
  - Hover for detailed information
</Accordion>

<Accordion title="Timeline View">
  The timeline displays:
  - Search progression
  - Performance trends
  - Discovery milestones
  - Convergence patterns
</Accordion>

<Accordion title="Control Panel">
  Key controls include:
  - Parameter adjustments
  - Visualization options
  - Export tools
  - Search controls
</Accordion>

## Common Issues

<Warning>
  Make sure both backend (port 8000) and frontend (port 8501) servers are running and accessible.
</Warning>

<Tabs>
  <Tab title="Dashboard Issues">
    <Steps>
      1. Check if both servers are running
      2. Verify port availability
      3. Check browser console
      4. Clear browser cache
    </Steps>
  </Tab>
  
  <Tab title="Search Problems">
    <Steps>
      1. Verify search space configuration
      2. Check resource availability
      3. Monitor system logs
      4. Review error messages
    </Steps>
  </Tab>
</Tabs>

## Next Steps

<Check>
  Ready to dive deeper? Explore these resources:
  - [Architecture Representation](/research/sphere-metaphor)
  - [Visualization Features](/guides/visualize-results)
  - [Result Interpretation](/guides/interpret-outcomes)
  - [Custom Experiments](/guides/run-experiments)
</Check>

<Info>
  Need help? Join our [Discord community](https://discord.gg/neuromosaic) or check our [GitHub Issues](https://github.com/neuromosaic/neuromosaic/issues).
</Info>
