---
icon: cloud
description: Learn how to develop applications with our ML platform
---

# Infrastructure
For local development, we offer two deployment options: local Docker-based and on-premises installations. Let me explain the key differences and benefits of each approach:

Local Development with K3D:
- Runs a lightweight Kubernetes cluster inside Docker containers
- Perfect for development and testing on your personal machine
- Easy to set up and tear down
- Minimal resource overhead
- Built on top of K3S, providing compatibility and consistency

On-Premises with K3S:
- Full Kubernetes distribution optimized for production workloads
- Ideal for dedicated hardware and GPU setups
- Production-grade security and stability
- Reduced resource footprint compared to standard K8s
- Same underlying technology as K3D for seamless transitions

Both options provide a complete Kubernetes experience while being optimized for their respective use cases. The shared K3S foundation ensures that your applications will behave consistently across environments.

# k3D local 
Before getting started with k3d, ensure you have the following prerequisites installed:

1. [uv package manager](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
2. [Docker](https://docs.docker.com/get-docker/) - Container runtime (minimum version 20.10.5)
3. Docker daemon - Use either:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for Windows/Mac)
   - [OrbStack](https://orbstack.dev/) (for Mac)
   - Docker Engine (for Linux)
4. [k3d](https://k3d.io/stable/#installation) - Install via:
5. [Helm](https://helm.sh/docs/intro/install/) - Package manager for Kubernetes
6. TODO : [gcloud CLI](https://cloud.google.com/sdk/docs/install) (Optional) - Recommended for cloud storage integration with Google Cloud Storage. Install this if you need to handle large datasets or artifacts. It enables efficient data transfer and management between your local environment and cloud storage. if you decieded to use cli checkout the infrastructure cloud section to know how to create an storage.


# Local Task Commands Documentation


This repository leverages task files to automate various processes, streamlining the setup and management of your cloud instances. To get started with initiating your instances on the cloud, follow the steps below:

1. To begin, create a virtual environment and enable the use of task files by running the following command:
   ```bash
   uv sync
   ```
   Alternatively, you can install the task tool directly without using Python. If you choose this method, use the `task` command instead of `uv run task`.

2. Run the following command to initiate your cloud instances. These are task files that need to be run with `uv run task ...`:
   ```bash
   uv run task local:initiate-storage
   ```

3. To install all the necessary extensions required for running LM Orbits, execute the following command. These are task files that need to be run with `uv run task ...`:
   ```bash
   uv run task local:initiate-k8s
   ```.

By following these steps, you will have your cloud infrastructure up and running efficiently. below you can find in detail infromation of available tasks

## Cluster Management
- **`local:cluster-create`**: Create a k3d cluster and install essential components.
- **`local:cluster-delete`**: Delete the k3d cluster.
- **`local:cluster-start`**: Start a stopped cluster.
- **`local:cluster-stop`**: Stop a running cluster.
- **`local:cluster-status`**: Check the overall cluster status.
- **`local:cluster-test`**: Create a test cluster.

## Deployment & Installation
- **`local:install-ingress`**: Install nginx ingress controller.
- **`local:install-kuberay`**: Install KubeRay operator.
- **`local:install-kuberay-cluster`**: Install Ray cluster.
- **`local:install-kuberay-job`**: Install Ray job sample.
- **`local:install-kuberay-service`**: Install Ray service.
- **`local:install-mlflow`**: Install or upgrade MLflow server.
- **`local:install-nessie`**: Install Project Nessie.
- **`local:install-zenml`**: Install or upgrade ZenML server.
- **`local:install-dremio`**: Install Dremio using Helm.

## Authentication & Configuration
- **`local:add-gcs-secret`**: Add Google Cloud Storage credentials.
- **`local:gcloud-auth`**: Configure Google Cloud authentication.

## Debugging & Monitoring
- **`local:check-ingress`**: Check ingress status.
- **`local:check-mlflow`**: Check MLflow deployment status.
- **`local:check-zenml`**: Check ZenML deployment status.
- **`local:debug`**: Create a debug pod for troubleshooting.

## Port Forwarding
- **`local:mlflow-port-forward`**: Forward MLflow server port to localhost.
- **`local:zenml-port-forward`**: Forward ZenML server port to localhost.

## GPU & Hardware
- **`local:gpu-cluster`**: Install NVIDIA GPU operator.
