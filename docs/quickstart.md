---
title: "Quickstart"
description: "Get up and running with NeuroMosaic in minutes"
---

# Quickstart Guide

Get NeuroMosaic running in three simple steps.

## 1. Installation

```bash
git clone https://github.com/yourusername/neuromosaic.git
cd neuromosaic
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Launch

```bash
# Terminal 1: Start backend
uvicorn backend.main:app --reload

# Terminal 2: Start frontend
cd frontend
streamlit run app.py
```

## 3. Run Your First Search

1. Open `http://localhost:8501`
2. Go to "Configuration" tab
3. Choose architecture type
4. Click "Start Exploration"

## Next Steps

- [Full Setup Guide](/guides/getting-started)
- [Visualization Guide](/guides/visualize-results)
- [Run Experiments](/guides/run-experiments)
