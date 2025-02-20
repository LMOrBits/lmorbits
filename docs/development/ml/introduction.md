# ML Package Development

## Overview
The ML package contains model training, evaluation, and inference code.

## Directory Structure
```
ml/
├── src/
│   ├── models/        # Model definitions
│   ├── training/      # Training pipelines
│   ├── evaluation/    # Model evaluation
│   └── inference/     # Inference logic
├── tests/
│   ├── unit/
│   └── integration/
└── configs/           # Model configurations
```

## Development Guidelines

### Model Development
- Use type hints
- Document model architecture
- Track experiments with MLflow

### Example Model Class
```python
from ml.base import BaseModel

class CustomModel(BaseModel):
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the model.
        
        Args:
            X: Training features
            y: Training labels
        """
        self.validate_input(X, y)
        # training logic
```

### Testing
- Test model convergence
- Validate model outputs
- Check memory usage