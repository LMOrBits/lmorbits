# ML Pipeline

## Overview

The ML pipeline manages model training, evaluation, and deployment workflows.

## Pipeline Stages

1. **Data Preparation**
   - Feature selection
   - Train/test split
   - Data normalization

2. **Model Training**
   - Hyperparameter tuning
   - Cross-validation
   - Model selection

3. **Evaluation**
   - Metrics calculation
   - Performance analysis
   - Model validation

4. **Deployment**
   - Model packaging
   - Version control
   - Deployment automation

## Usage Example

```python
from ml.pipeline import MLPipeline

pipeline = MLPipeline(
    model_config="configs/model.yaml",
    data_config="configs/data.yaml"
)

pipeline.train()
pipeline.evaluate()
pipeline.deploy()
```

## Experiment Tracking

We use MLflow for experiment tracking:
- Model parameters
- Metrics
- Artifacts 