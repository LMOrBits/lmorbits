---
icon: robot
description: Guide for machine learning development
---
# ML Package

The ML package is responsible for all machine learning operations in our project, including model training, evaluation, and experimentation.

## Package Structure

```
ml/
├── configs/         # Model and training configurations
├── notebooks/       # Jupyter notebooks for experimentation
├── scripts/         # Utility and automation scripts
├── src/            # Main source code
├── test/           # Test files
├── Taskfile.yaml   # Task automation definitions
├── Makefile        # Build and development commands
└── pyproject.toml  # Package dependencies and configuration
```

## Key Features

### 1. Model Management

The package supports various ML models and operations:
- LLaMA model integration via `llama-cpp-python`
- MLflow for experiment tracking
- Unsloth for model optimization (optional)
- Google Cloud Storage integration for model storage

### 2. Development Tools

The package includes several development tools:
- Task automation via `Taskfile.yaml`
- Build commands via `Makefile`
- Code quality tools (ruff for linting and formatting)
- Jupyter notebook support for experimentation

### 3. Package Dependencies

Key dependencies include:
- `llama-cpp-python`: LLaMA model integration
- `mlflow`: Experiment tracking and model registry
- `omegaconf`: Configuration management
- `google-cloud-storage`: Cloud storage integration
- `data`: Internal data package integration

## Configuration

### Environment Setup

The package supports Python 3.10-3.13 and requires specific dependencies:
```bash
# Install base dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Model Configuration

Models are configured using OmegaConf in the `configs/` directory:
```yaml
# Example model configuration
model:
  name: llama
  version: 2
  parameters:
    # model specific parameters
```

## Usage

### Setting Up

1. Install dependencies:
```bash
make install
```

2. Configure environment:
```bash
# Set up necessary environment variables
export GOOGLE_CLOUD_PROJECT=...
export MLFLOW_TRACKING_URI=...
```

### Running Experiments

Use the task runner for common operations:
```bash
task train-model
task evaluate-model
task export-model
```

## Best Practices

1. **Model Development**
   - Use notebooks for experimentation
   - Keep configurations version controlled
   - Document model architectures and decisions

2. **Code Organization**
   - Follow modular design principles
   - Implement proper testing
   - Use type hints for better code quality

3. **Experiment Tracking**
   - Use MLflow for all experiments
   - Log all relevant metrics
   - Document experiment configurations

## Integration with Other Packages

The ML package integrates with:
- `data`: For dataset management and preprocessing
- `orchestration`: For pipeline integration
- `serve`: For model serving preparation

## Development Workflow

1. **Experimentation**
   - Use Jupyter notebooks in `notebooks/`
   - Track experiments with MLflow
   - Document findings and decisions

2. **Implementation**
   - Move successful experiments to source code
   - Implement proper testing
   - Follow code quality guidelines

3. **Deployment**
   - Prepare models for serving
   - Version models appropriately
   - Document deployment requirements

## Troubleshooting

Common issues and solutions:
1. **Model Training Issues**
   - Check GPU availability
   - Verify data pipeline
   - Monitor resource usage

2. **Integration Problems**
   - Check dependency versions
   - Verify configuration files
   - Review integration points

3. **Development Environment**
   - Verify Python version
   - Check dependency conflicts
   - Ensure proper tool installation

