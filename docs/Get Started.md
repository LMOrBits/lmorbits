# Getting Started

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/Parsa-Mir/lmorbits)

Welcome to our project documentation! This guide will help you set up and start using the project quickly.

## Prerequisites

Before you begin, ensure you have the following installed:
- uv (python package manager) if not installed, install it with `pip install uv`
- Git

## Quick Start

1. **Clone the Repository**
   ```sh
   git clone https://github.com/Parsa-Mir/lmorbits.git
   cd lmorbits
   ```

2. **Set Up Development Environment**
   
   ```sh
   code <your working space>.workspace
   ```
   ```sh
   uv sync --only-group <group name>
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
