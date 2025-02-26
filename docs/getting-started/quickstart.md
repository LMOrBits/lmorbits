---
icon: rocket
description: Get started with LMOrbits 
---
# Introduction
LMOrbits is a Package for building and deploying Small language models. This document provides a quick start guide to help you get familiar with it quickly.

# Quick Start Guide


## Prerequisites

Make sure you have:
- Completed the [installation](installation.md)
- Access to required credentials
- Basic understanding of Python

## First Steps

1. **Configure Your Environment**
   ```sh
   # Set up environment variables
   export API_KEY="your-api-key"
   export MODEL_PATH="/path/to/models"
   ```

2. **Run Your First Pipeline**
   ```python
   from ml.pipeline import Pipeline
   
   # Initialize pipeline
   pipeline = Pipeline()
   
   # Run basic workflow
   pipeline.run("example_workflow")
   ```

3. **Check the Results**
   ```python
   # View pipeline outputs
   pipeline.get_results()
   ```

## Common Tasks

### Training a Model
```python
from ml.training import Trainer

trainer = Trainer()
trainer.train(data_path="data/training.csv")
```

### Making Predictions
```python
from ml.predict import Predictor

predictor = Predictor(model_path="models/latest")
predictions = predictor.predict(data)
```

### Using the API
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"data": your_data}
)
```

## Next Steps

- Explore [ML Development](../how-to/development/ml.md)
- Learn about [Data Processing](../how-to/development/data.md)
- Check [API Development](../how-to/development/api.md) 