---
icon: download
description: Install and set up the project environment
---

# Installation

## Prerequisites

Before you begin, ensure you have:
- Python 3.12 or higher
- pip (Python package installer)
- Git

## Step-by-Step Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/your-project.git
   cd your-project
   ```

2. **Set Up Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Project Structure
```
packages/
├── data/         # Data processing
├── ml/           # ML models
├── serve/        # API components
└── orchestration/# Workflows
```

## Next Steps

- Follow our [Quick Start Guide](quickstart.md)
- Check [Development Guide](../how-to/development/README.md) 