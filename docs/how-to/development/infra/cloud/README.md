---
icon: cloud
---

# Infrastructure
To set up the cloud infrastructure, we will be using Terraform and Helm. Before we begin, there are essential prerequisites you need to have:

1. [uv package manager](https://github.com/astral-sh/uv) - Fast Python package installer and resolver.
2. [gcloud CLI](https://cloud.google.com/sdk/docs/install) - Command-line interface for Google Cloud Platform.
3. [kubectl](https://kubernetes.io/docs/tasks/tools/) - Kubernetes command-line tool.
4. [Helm](https://helm.sh/docs/intro/install/) - Package manager for Kubernetes.
5. [Terraform](https://developer.hashicorp.com/terraform/downloads) - Infrastructure as Code tool.
6. [Civo CLI](https://www.civo.com/docs/overview/civo-cli) - Command-line tool for managing Civo cloud resources.
7. [Docker](https://docs.docker.com/get-docker/) - Container runtime (minimum version 20.10.5)
8. [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for Windows/Mac)

Once you have these tools ready, we can proceed with the implementation. Our cloud infrastructure will primarily rely on the artifact registry, storage, and GPU access. These components are crucial for managing and optimizing our cloud resources effectively.


## Qucik Start 

This repository leverages task files to automate various processes, streamlining the setup and management of your cloud instances. To get started with initiating your instances on the cloud, follow the steps below:

1. To begin, create a virtual environment and enable the use of task files by running the following command:
   ```bash
   uv sync
   ```
   Alternatively, you can install the task tool directly without using Python. If you choose this method, use the `task` command instead of `uv run task`.

2. Run the following command to initiate your cloud instances. These are task files that need to be run with `uv run task ...`:
   ```bash
   uv run task cloud:initiate-iac
   ```
   This command initiates the IaC development environment. Ensure you have the correct variables set in your .env file (based on the .env.example file and tfvars file).

3. To install all the necessary extensions required for running LM Orbits, execute the following command. These are task files that need to be run with `uv run task ...`:
   ```bash
   uv run task cloud:initiate-k8s
   ```
   This command installs all extensions and creates all resources needed for LM Orbits.

By following these steps, you will have your cloud infrastructure up and running efficiently.


## Dive Deeper

As previously mentioned, we are using Taskfile, and in order to go into the deeper understanding of what are the tasks that is being used or underlying the current implementation, we can use the command below to list them all. And in order to go, here you can see all of the current state of the tasks that we are using. And in order to get even more into depth, we will divide it into the two sections of the K8S, basically, and also the infrastructure as a code task, so to make it clear for us what is going on underneath.

### Infrastructure as Code (IaC)

- **`cloud:iac:init-dev-environment`**  
  Initializes and applies Terraform configurations for the development environment based on the `terraform.tfvars` file in the `environment/dev` directory.

- **`cloud:iac:initiate-backend-storage`**  
  Creates and configures a Google Cloud Storage bucket for Terraform backend.  
  - Sets up a required GCS bucket for state files with versioning enabled.  
  - Must be run before initializing any environment.

- **`cloud:initiate-iac`**  
  Initiates the IaC development environment.  
  - Requires a `.env` file with correct variables (based on the `.env.example` file and `tfvars` file).

- **`cloud:initiate-k8s`**  
  Installs all extensions and creates all required resources for LMOrbits.

### Kubernetes
#### Kubernetes Extensions - Ingress Controller

- **`cloud:k8s:extensions:ingress:debug-ingress`**  
  Debugs ingress configuration and logs.

- **`cloud:k8s:extensions:ingress:install-ingress`**  
  Installs the Nginx ingress controller.

- **`cloud:k8s:extensions:ingress:status-ingress`**  
  Checks ingress status.

#### Kubernetes Extensions - KubeRay

- **`cloud:k8s:extensions:kuberay:install`**  
  Installs the KubeRay operator.

- **`cloud:k8s:extensions:kuberay:install-cluster`**  
  Installs a KubeRay cluster.

- **`cloud:k8s:extensions:kuberay:install-job`**  
  Installs a KubeRay job sample.

- **`cloud:k8s:extensions:kuberay:install-service`**  
  Installs a KubeRay service sample.

- **`cloud:k8s:extensions:kuberay:port-forward`**  
  Sets up port forwarding for the KubeRay cluster.

- **`cloud:k8s:extensions:kuberay:status`**  
  Checks the status of KubeRay jobs and clusters.

- **`cloud:k8s:extensions:kuberay:uninstall-cluster`**  
  Uninstalls the KubeRay cluster.

- **`cloud:k8s:extensions:kuberay:uninstall-job`**  
  Uninstalls a KubeRay job.

- **`cloud:k8s:extensions:kuberay:uninstall-service`**  
  Uninstalls a KubeRay service.

#### Kubernetes Extensions - MLflow

- **`cloud:k8s:extensions:mlflow:install`**  
  Installs or upgrades the MLflow server.

- **`cloud:k8s:extensions:mlflow:port-forward`**  
  Port forwards MLflow server to `localhost:5000`.

- **`cloud:k8s:extensions:mlflow:status`**  
  Checks MLflow deployment status.

#### Kubernetes Extensions - Optik

- **`cloud:k8s:extensions:optik:install`**  
  Installs Optik.

#### Kubernetes Extensions - ZenML

- **`cloud:k8s:extensions:zenml:install`**  
  Installs or upgrades the ZenML server.

- **`cloud:k8s:extensions:zenml:port-forward`**  
  Port forwards the ZenML server to `localhost:8080`.

- **`cloud:k8s:extensions:zenml:status`**  
  Checks ZenML deployment status.

#### Kubernetes Extensions - GCloud Integrations

- **`cloud:k8s:gcloud:add-gcs-secret-lakefs`**  
  Creates GCS credentials secret for LakeFS.

- **`cloud:k8s:gcloud:docker-auth`**  
  Creates a Docker registry secret for the default namespace.

- **`cloud:k8s:gcloud:docker-auth-zen`**  
  Creates a Docker registry secret for the ZenML namespace.

- **`cloud:k8s:gcloud:gcloud-docker-auth`**  
  Creates a Docker registry secret for the default namespace.

- **`cloud:k8s:gcloud:gcloud-docker-auth-zen`**  
  Creates a Docker registry secret for the ZenML namespace.

#### Kubernetes Utilities

- **`cloud:k8s:utils:debug`**  
  Creates and accesses a debug pod in the ZenML namespace.

- **`cloud:k8s:utils:delete-debug`**  
  Deletes the debug pod in the ZenML namespace.
