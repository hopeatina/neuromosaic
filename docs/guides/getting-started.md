---
title: "Getting Started"
description: "Set up Neuromosaic and run your first architecture exploration"
---

<Note>
  Welcome to Neuromosaic! This guide will help you set up the platform and run your first neural architecture exploration experiment.
  Some features described here are planned for future releases.
  
  View the full documentation at [https://neuromosaic.mintlify.app/](https://neuromosaic.mintlify.app/)
</Note>

## Quick Setup

<Steps>
  1. **Clone the Repository**
     ```bash
     git clone https://github.com/hopeatina/neruromosaic/neuromosaic.git
     cd neuromosaic
     ```

2.  **Create Environment**
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

3.  **Start Services**
    ````bash # Start the API server
    python -m neuromosaic serve-api
         # In a new terminal, start the dashboard (Coming Soon)
         python -m neuromosaic dashboard
         ```
    </Steps>
    ````

## Running Your First Search

<CardGroup cols={2}>
  <Card title="Quick Start" icon="play">
    ```bash
    # Basic search with defaults
    python -m neuromosaic quickstart
    
    # With GPU support
    python -m neuromosaic quickstart --gpu
    
    # Custom output directory
    python -m neuromosaic quickstart --output-dir my_search
    ```
  </Card>
  
  <Card title="Custom Search" icon="sliders">
    ```bash
    # Create and edit config.yaml
    # Then run:
    python -m neuromosaic experiment \
      --config config.yaml \
      --output-dir custom_search
    ```
  </Card>
</CardGroup>

## Available Commands

<CardGroup cols={2}>
  <Card title="Core Commands" icon="terminal">
    Available Now:
    - `quickstart`: Quick exploration
    - `experiment`: Custom searches
    - `analyze`: Basic analysis
    - `serve-api`: Start API server
  </Card>
  
  <Card title="Additional Tools" icon="toolbox">
    Available Now:
    - `inspect`: View architectures
    
    Coming Soon:
    - `dashboard`: Interactive UI
    - Advanced analysis tools
  </Card>
  
  <Card title="Configuration" icon="gear">
    Available Now:
    - Basic search settings
    - Resource configuration
    
    Coming Soon:
    - Advanced optimization
    - Distributed setup
  </Card>
  
  <Card title="Monitoring" icon="gauge">
    Available Now:
    - Basic logs
    - Status checks
    
    Coming Soon:
    - Real-time monitoring
    - Performance tracking
  </Card>
</CardGroup>

## Common Operations

<Tabs>
  <Tab title="Basic Search">
    ```bash
    # Quick start with defaults
    python -m neuromosaic quickstart
    
    # View results
    python -m neuromosaic analyze results_dir
    ```
  </Tab>
  
  <Tab title="Custom Search">
    ```bash
    # Run with configuration
    python -m neuromosaic experiment \
      --config config.yaml \
      --output-dir custom_search
    
    # Resume previous run
    python -m neuromosaic experiment \
      --config config.yaml \
      --resume
    ```
  </Tab>
</Tabs>

## Monitoring & Debugging

<Warning>
  Basic monitoring is available through logs and status checks.
  Interactive dashboard and advanced monitoring features are under development.
</Warning>

<Steps>
  1. **Check Status**
     ```bash
     # View API server status
     curl http://localhost:8000/health
     
     # Check experiment status
     python -m neuromosaic experiment --config config.yaml --status
     ```

2.  **View Logs**

    ```bash
    # Check application logs
    tail -f neuromosaic.log
    ```

3.  **Monitor Resources**
    Available Now: - Basic system monitoring - Log-based tracking
    Coming Soon: - Real-time resource monitoring - Performance analytics
    </Steps>

## Common Issues

<Accordion title="API Server">
  - Check if server is running on port 8000
  - Verify environment activation
  - Review error messages in logs
  - Check network connectivity
</Accordion>

<Accordion title="Search Configuration">
  - Validate YAML syntax
  - Check resource settings
  - Verify file paths
  - Review permissions
</Accordion>

## Next Steps

<Check>
  Ready to explore more?
  
  Available Now:
  - [Run custom experiments](https://neuromosaic.mintlify.app/guides/run-experiments)
  - Basic result analysis
  
  Coming Soon:
  - [Interactive visualization](https://neuromosaic.mintlify.app/guides/visualize-results)
  - [Advanced analysis](https://neuromosaic.mintlify.app/guides/interpret-outcomes)
  
  Note: Some features mentioned in the documentation are still under development.
</Check>

<Info>
  Need help? Join our [Discord community](https://discord.gg/neuromosaic) or check our [GitHub Issues](https://github.com/hopeatina/neruromosaic/neuromosaic/issues).
  
  Full documentation: [https://neuromosaic.mintlify.app/](https://neuromosaic.mintlify.app/)
</Info>
