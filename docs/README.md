---
icon: house
description: Welcome to our project documentation. Get started with our ML platform.
---

# LMOrbits Project Documentation

Welcome to the LMOrbits project documentation. This documentation provides comprehensive information about the project structure, setup, and development guidelines.

## Project Structure

The project is organized into several specialized packages, each with its own responsibility:

### Core Packages

1. **Orchestration Package**
   - Manages workflow orchestration using ZenML
   - Handles pipeline definitions and execution
   - Provides development and production environment configurations
   - Uses Task files and Makefiles for automation

2. **ML Package**
   - Contains machine learning models and algorithms
   - Handles model training and evaluation
   - Includes Jupyter notebooks for experimentation
   - Manages model configurations and hyperparameters

3. **Data Package**
   - Responsible for data processing and management
   - Handles data validation and transformation
   - Provides data pipeline implementations
   - Manages data configurations and schemas

4. **Application Package**
   - Implements application logic and business rules
   - Handles API implementations
   - Manages application state and configurations

5. **Serve Package**
   - Handles model serving and deployment
   - Manages API endpoints for model inference
   - Implements serving configurations

## Why ZenML for Orchestration?

We chose ZenML as our orchestration framework for several key reasons:
- Lightweight and easy to use
- Excellent support for ML pipelines
- Built-in support for experiment tracking
- Flexible deployment options
- Strong integration capabilities with various ML tools

## Development Environments

The project supports multiple development environments:

1. **Development Stage**
   - Local development environment
   - Development-specific configurations
   - Hot-reloading and debugging support

2. **Production Stage**
   - Production-grade configurations
   - Optimized for performance
   - Enhanced security measures

3. **Utils**
   - Shared utilities and helper functions
   - Common tools and scripts
   - Development tools and automation scripts

## Automation and Scripts

Each package contains its own:
- `Taskfile.yml` for task automation
- `Makefile` for build and development commands
- Custom scripts for package-specific operations

## Documentation Structure

This documentation is organized using GitBook for better readability and navigation. You'll find:
- Getting Started guides
- How-to guides for each package
- Development guidelines
- API documentation
- Best practices and conventions

Navigate through the sidebar to explore specific topics in detail.

## Quick Navigation

- [Installation](getting-started/installation.md) - Set up the project
- [Quick Start Guide](getting-started/quickstart.md) - Get running in minutes
- [Development Guide](how-to/development/README.md) - Start developing
- [API Reference](reference/api/README.md) - API documentation

## Need Help?

- 📝 Open an issue in our GitHub repository
- 💬 Join our community Discord
- 📧 Contact support@example.com 