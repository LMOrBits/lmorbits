---
icon: code
description: Learn how to develop with our ML platform
---

### LMOrbits
Here, we focus on the dynamic management and operation of Small Language Models (SLMs). Our package is structured into five distinct yet interconnected components, each designed to be developed independently while contributing to the overall functionality of the system.

1. **Applications**: This package embodies the core concepts of chains and agents within Small Language Models, allowing you to create innovative applications that leverage the power of SLMs.

2. **Data**: The Data package is your go-to for managing data operations. It provides a robust framework for handling data processing, ensuring that your data is always ready for use.

3. **ML**: The ML package is where the magic happens! Here, you can fine-tune your models, perform evaluations, track experiments, and manage inference processes. It’s designed to streamline your machine learning workflows and enhance your experimentation capabilities.

4. **Orchestration**: At the heart of our system lies the Orchestration package, powered by ZenML. This component manages the entire workflow, organizing everything from development to production. It features dedicated folders for development, production, and staging, each equipped with its own pipeline to ensure smooth operations.

5. **Serve**: Finally, the Serve package is responsible for deploying your models. Depending on your specific needs, you can serve your models in various environments, making it a flexible and essential part of the architecture.

Each of these packages is crafted to work seamlessly together, allowing teams to collaborate effectively while focusing on their individual areas of expertise. Get ready to dive in and explore the limitless possibilities of LMOrbits!

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

## Development Areas

- [ML Development](ml.md) - Build and train models
- [Data Processing](data.md) - Handle data pipelines
- [API Development](api.md) - Create and manage APIs
- [Orchestration](orchestration.md) - Manage workflows

## Getting Started

1. Set up your development environment
2. Follow our coding standards
3. Write tests for your code
4. Submit pull requests

## Best Practices

- Follow [Code Standards](../best-practices/code-standards.md)
- Write comprehensive tests
- Document your code
- Review our [Contributing Guide](../../reference/contributing.md) 