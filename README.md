# NeuraMosaic

NeuraMosaic is a research and development platform that explores and optimizes novel neural network architectures—ranging from standard transformer models to brain-inspired designs—using a combination of automated code generation (via Large Language Models), compositional search spaces, and meta-learning.

The core idea is to represent each architecture as a structured vector in a flexible "architecture embedding space." This space defines what building blocks a model is made of, how they fit together, and the numeric 'magic numbers' (hyperparameters) that shape their behaviors. NeuraMosaic then uses these vector representations to automatically generate code for new architectures, train and evaluate them on small tasks, and learn which directions in this space are most promising. Over time, it refines its search, guided by performance metrics and insights from research literature.

## In short:

NeuraMosaic helps you discover, understand, and evolve custom neural architectures, blending automated code generation with systematic exploration to find better models efficiently.

## Why NeuraMosaic?

- **Composable Architectures**: Move beyond predefined sets of layers and architectures.
- **Automated Code Generation**: Turn architecture "vectors" directly into runnable model code via LLM prompts.
- **Meta-Learning & Visualization**: Collect performance results, create heatmaps and embeddings of architectural performance, and use them to guide future searches.
- **Inspiration from Literature**: Seamlessly integrate known components from cutting-edge papers, enabling continuous innovation.
- **Reproducibility & Versioning**: Every generated code snippet, environment, and experimental result is tracked and can be re-run or analyzed at any time.

## Target Users

- **ML Researchers & Practitioners** who want to quickly test a broad range of model variations.
- **AutoML Enthusiasts** seeking to push beyond standard hyperparameter tuning into architecture-level exploration.
- **Developers** interested in LLM-Driven Code Generation as a practical application of generative AI to improve ML workflows.

## Project Goals

### Flexible Architecture Representation:

Represent neural models as vectors that encode building blocks (attention types, feedforward variants, normalization layers) and hyperparameters (hidden sizes, number of layers).

### Scalable Automated Pipeline:

Given an architecture vector, automatically generate the model code with LLMs, containerize it, train it on small tasks, evaluate results, and store metrics.

### Guided Search and Meta-Learning:

Visualize performance "heatmaps" over the architecture space, identify promising regions, and refine the search strategy. Meta-learning guides which architectures to explore next.

### Incorporate Brain-Inspired and Literature-Based Components:

Easily introduce new, exotic modules (e.g., feedback loops, Hebbian updates, sparse activations) inspired by neuroscience or recent papers.

### Reproducibility & Version Control:

Track all experiments, versions of generated code, and environment details. Re-run and verify results anytime.

## MVP (Minimum Viable Product)

1. **Compositional Encoding**: A basic schema to encode architectures into a vector form, including a few standard transformer variations and a simple brain-inspired module.
2. **LLM-Assisted Code Generation**: A prompt template and workflow to generate PyTorch code from a given architecture vector using a local LLM (like LLaMA) or an external API (e.g., GPT-4).
3. **Lightweight Training Loop**: Train and evaluate each architecture on a tiny dataset (e.g., toy language modeling) and record performance metrics (loss, perplexity).
4. **Results Database & Visualization**: Store results (configurations, metrics) in a local database. Generate a 2D projection plot of the architecture space color-coded by performance.
5. **Simple Orchestration**: Run a small set of experiments asynchronously using containers (Docker) and a Python script to manage them.

## 6-Month Roadmap

### Month 1-2: Foundation & MVP

- Implement the initial vector encoding for a small set of known architectures (e.g., Transformer variants).
- Set up LLM integration for code generation.
- Run first experiments and store results in a local SQLite database.
- Create simple visualization tools (2D projections, metrics dashboards).

### Month 3-4: Expanding Search & Meta-Learning

- Integrate Bayesian optimization or evolutionary search to guide architecture selection.
- Add basic brain-inspired modules (e.g., feedback connections, mixture-of-experts).
- Implement meta-learning to prune unhelpful search directions and focus on promising areas.
- Introduce a version-control scheme for generated code (Git integration) and container tags.

### Month 5: Literature Integration & Enhanced Visualization

- Build a small knowledge base of known architectural innovations from recent papers.
- Prompt LLM to incorporate these new components into candidate architectures.
- Add interactive visualizations: heatmaps of performance, cluster analysis of architectures, and layered detail views.

### Month 6: Scaling & Refinement

- Optimize training loops and possibly run multiple experiments in parallel.
- Refine the code generation prompts and templates for better reliability.
- Validate system by discovering a novel architecture that outperforms a known baseline on the test tasks.
- Document best practices and finalize a stable API for external contributions.

## System Architecture Diagram

Below is a high-level view of how all components interact:

```scss
               ┌─────────────────────────┐
               │       User Interface     │
               │ (CLI, Notebook, Dashboards)
               └─────┬───────────────────┘
                     │
                     v
         ┌──────────────────────┐
         │      Orchestrator     │
         │ (Python Control Loop) │
         └───────┬──────────────┘
                 │
                 │ Suggest New Architecture Vector
                 v
       ┌─────────────────────┐
       │   Architecture       │
       │   Vector Space       │
       │   Representation     │
       └───────┬─────────────┘
               │ Converts Vector to Prompt
               v
       ┌─────────────────────┐
       │     LLM Code Gen     │
       │ (Local LLaMA / GPT-4)│
       └───────┬─────────────┘
               │ Generated Code
               v
       ┌─────────────────────┐
       │   Environment &     │
       │   Container Manager │
       │  (Docker, etc.)     │
       └───────┬─────────────┘
               │  Run Training/Eval
               v
       ┌─────────────────────┐
       │ Training & Eval      │
       │(PyTorch Model + Task)│
       └───────┬─────────────┘
               │ Metrics & Logs
               v
       ┌─────────────────────┐
       │ Results Database     │
       │ (SQLite, JSON)       │
       └───────┬─────────────┘
               │
               │ Queries & Retrieval
               v
       ┌─────────────────────┐
       │ Meta-Learning &      │
       │ Visualization Tools  │
       │(Analysis Scripts,    │
       │ Heatmaps, Projections│
       └───────┬─────────────┘
               │
     Feedback  │ Updates
       Loop    v
      ┌─────────────────────┐
      │ Updated Search       │
      │ Strategy (BayesOpt,  │
      │ Evo Alg, etc.)       │
      └─────────────────────┘
```

## Interactive Dashboard

NeuraMosaic includes a powerful web-based dashboard for visualizing and interacting with the architecture search space. The dashboard provides real-time insights into experiments, architecture performance, and search progress.

### Key Features

- **3D Architecture Space Visualization**: Explore the architecture search space in an interactive 3D view, where each point represents an experiment. Points are color-coded by performance metrics.
- **Real-time Experiment Monitoring**: Track ongoing experiments and view their progress in real-time.
- **Detailed Architecture Analysis**: Click on any point to see detailed information about the architecture, including:
  - Performance metrics (accuracy, loss, perplexity)
  - Architecture components and structure
  - Training history and evolution
- **Experiment Control**: Launch new experiments directly from the dashboard with customized parameters.
- **Metric Filtering & Comparison**: Filter and compare architectures based on different metrics and complexity measures.

### Using the Dashboard

1. Start the dashboard server:

```bash
python -m neuromosaic dashboard
```

2. Open your browser and navigate to `http://localhost:8050` (default port).

3. The dashboard interface is organized into:

   - Left sidebar: Controls for filtering and launching experiments
   - Main view: 3D visualization of the architecture space
   - Detail panel: Information about selected architectures

4. Interact with the visualization:
   - Rotate and zoom the 3D plot
   - Click points to see architecture details
   - Use filters to focus on specific metrics or complexity ranges
   - Launch new experiments with the control panel

### Technical Details

The dashboard is built using:

- Dash and Plotly for interactive visualizations
- Bootstrap for responsive layout
- FastAPI for backend communication
- SQLAlchemy for database integration

For more details on extending or customizing the dashboard, see the [Frontend Development Guide](docs/frontend.md).
