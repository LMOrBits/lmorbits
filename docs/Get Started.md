# Getting Started

Welcome to our project documentation! This guide will help you set up and start using the project quickly.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.12 or higher
- `pip` (Python package installer)
- Git

## Quick Start

1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/your-project.git
   cd your-project
   ```

2. **Set Up Development Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Project Structure**
   ```
   packages/
   ├── data/         # Data processing and management
   ├── ml/           # Machine learning models and training
   ├── serve/        # API and serving components
   └── orchestration/# Workflow orchestration
   ```

## Next Steps

- Read the [Architecture Overview](./architecture.md) to understand the system design
- Check out our [Development Guide](./development-guide.md) for coding standards
- See [API Documentation](./api-reference.md) for available endpoints
- Review [ML Pipeline](./ml-pipeline.md) for model training workflow
