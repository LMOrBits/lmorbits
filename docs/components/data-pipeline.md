# Data Pipeline

## Overview

The data pipeline handles data ingestion, processing, and storage for our ML system.

## Components

### Data Ingestion
- Supported data sources
- Data validation
- Error handling

### Data Processing
- Feature engineering
- Data cleaning
- Transformation pipelines

### Data Storage
- Database schema
- Data versioning
- Access patterns

## Usage

```python
from data.pipeline import DataPipeline

pipeline = DataPipeline(config_path="config.yaml")
pipeline.run()
```

## Configuration

Example configuration:
```yaml
source:
  type: "csv"
  path: "data/raw/"
  
processing:
  cleaning: true
  feature_engineering: true
  
output:
  format: "parquet"
  path: "data/processed/"
``` 