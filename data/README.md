# Data Management

This directory contains datasets and instructions for data management in Neuromosaic.

## Directory Structure

```
data/
├── raw/                  # Original, immutable data dumps
├── processed/            # Cleaned and processed data ready for training
├── interim/             # Intermediate data that has been transformed
└── external/            # Data from third party sources
```

## Dataset Management

### Local Datasets

1. Place raw datasets in `data/raw/`
2. Run processing scripts from `scripts/data_processing/`
3. Processed data will be saved to `data/processed/`

### Remote Datasets

Some datasets are too large to store in the repository. These will be downloaded automatically when needed:

1. HuggingFace Datasets:

   ```python
   from neuromosaic.utils.storage_manager import fetch_dataset
   dataset = fetch_dataset("wikitext-103")
   ```

2. Custom Datasets:
   ```python
   from neuromosaic.utils.storage_manager import download_dataset
   download_dataset("https://example.com/dataset.zip", "custom_dataset")
   ```

## Storage Guidelines

1. **Raw Data**

   - Never modify raw data files
   - Include data source and version information
   - Document any data quality issues

2. **Processed Data**

   - Include processing scripts in `scripts/data_processing/`
   - Document transformations applied
   - Version processed datasets

3. **External Data**
   - Document data sources and licenses
   - Include fetch/download scripts
   - Cache downloaded data appropriately

## Data Versioning

We use DVC (Data Version Control) to track large files and datasets:

```bash
# Track a new dataset
dvc add data/raw/large_dataset.zip

# Push to remote storage
dvc push

# Pull latest datasets
dvc pull
```

## Access Control

1. **Public Datasets**

   - Available directly through the data fetchers
   - Cached locally in `data/external/`

2. **Private Datasets**
   - Require authentication
   - Set credentials in `.env` file:
     ```
     DATASET_API_KEY=your_key_here
     DATASET_USERNAME=your_username
     ```

## Adding New Datasets

1. Create a new directory in appropriate subdirectory
2. Add dataset documentation:

   - Source and version
   - License information
   - Processing steps
   - Usage examples

3. Update data fetchers if needed:
   ```python
   # In utils/storage_manager.py
   @register_dataset
   def fetch_new_dataset():
       """Fetch and prepare new dataset."""
       pass
   ```

## Artifacts Management

Model checkpoints and experiment artifacts are stored separately from datasets:

```python
from neuromosaic.utils.storage_manager import save_checkpoint

# Save model checkpoint
save_checkpoint(
    model,
    metrics,
    path="experiments/run_123/checkpoints/model_best.pt"
)
```

See `utils/storage_manager.py` for more details on artifact management.
