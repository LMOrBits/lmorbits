---
icon: house
description: Welcome to our project documentation. Get started with our ML platform.
---

# Welcome to LMOrbits

Welcome to LMOrbits! We are thrilled to introduce you to this amazing package designed for operating the small language models. Here, you'll find a clear structure to help you get started, along with detailed information about the project and its components. We can't wait for you to explore everything we have to offer and embark on your journey into the fascinating world of language models!


## Project Structure

To kick off your journey with our project, let's break it down into three exciting Git repositories! First up, we have the **Infrastructure as Code (IaC)** repository, which lays the groundwork for our infrastructure. Next, we dive into the **Operations** repository, where the magic happens as we manage and orchestrate our workflows. Finally, we have the **Application** repository, where you can find the application that utilizes the models in a tailored manner.

you can explore each of these core repositories one by one, as it contains the essential packages that power the entire logic of our project. Get ready to discover the building blocks of LMOrbits and how they come together to create a seamless experience!

1. **lmorbits**
   - This repository manages and orchestrates our workflows.
   - <img src="https://github.com/favicon.ico" alt="GitHub" width="16" height="16"/> [Operations Repository](https://github.com/example/operations)

2. **Infrastructure as Code (IaC)**
   - This repository lays the groundwork for our infrastructure.
   - <img src="https://github.com/favicon.ico" alt="GitHub" width="16" height="16"/> [IAC Repository](https://github.com/example/iac) 
   - Accessible within the operations repository.

3. **Application**
   - This repository is where you can develop amazing applications around the models.
   - <img src="https://github.com/favicon.ico" alt="GitHub" width="16" height="16"/> [Application Repository](https://github.com/example/application)


### IaC

Our infrastructure is designed to seamlessly support both cloud and local environments, making it versatile and user-friendly! For on-prem/local development, we utilize K3D/k3s, which allows you to easily set up a a light weight local Kubernetes environment on your system. This means you can test and develop the package  right from your machine/machines! However, some functionalities, such as using cloud GPUs, may not work in this setup unless you have GPUs available in the K3s or K3D cluster.

On the cloud side, we leverage Terraform to manage our infrastructure instances efficiently. Our primary focus is on Google Cloud and Civo, where we implement various modules, including IAM rules, to ensure secure access and management. We cover essential services such as Google Cloud Storage, Vertex AI, Virtual Private Cloud (VPC), service accounts, compute resources, Cloud Build, and the Artifact Registry.

Additionally, we support three distinct environments to cater to different stages of development. For Kubernetes system implementation, we use SIBO, which helps us initiate and manage cloud-native solutions effectively. This robust setup empowers you to build and deploy applications with confidence, whether locally or in the cloud!

### LMOrbits
LMOrbits focuses on the dynamic management and operation of Small Language Models (SLMs) through five interconnected components: Applications, which enable the creation of innovative SLM-based ; Data, which provides a robust framework for data processing; ML, where model fine-tuning, evaluations, and experiment tracking occur; Orchestration, powered by ZenML, that manages workflows across development, production, and staging; and Serve, responsible for deploying models in various environments. Together, these packages facilitate effective collaboration and enhance the overall functionality of the system, allowing users to explore the vast potential of LMOrbits.

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