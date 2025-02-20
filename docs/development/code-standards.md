# Code Standards

## Python Style Guide

- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Maximum line length: 88 characters (Black formatter default)
- Use docstrings for all public functions and classes

## Project Structure

```
packages/
├── data/         
│   ├── src/
│   └── tests/
├── ml/           
│   ├── src/
│   └── tests/
├── serve/        
│   ├── src/
│   └── tests/
└── orchestration/
    ├── src/
    └── tests/
```

## Naming Conventions

- Files: lowercase with underscores (e.g., `data_loader.py`)
- Classes: PascalCase (e.g., `DataLoader`)
- Functions/Variables: lowercase with underscores (e.g., `load_data`)
- Constants: uppercase with underscores (e.g., `MAX_BATCH_SIZE`)

## Testing Standards

- All code must have unit tests
- Maintain minimum 80% code coverage
- Use pytest for testing
- Mock external dependencies 