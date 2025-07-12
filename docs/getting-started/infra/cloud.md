---
icon: cloud
description: Learn how to develop applications with our ML platform
---

# Cloud Infrastructure Setup Guide

## Prerequisites

Before you begin, ensure you have the following tools installed:

- [gcloud](https://cloud.google.com/sdk/docs/install) - Google Cloud SDK
- [terraform](https://www.terraform.io/downloads) - Infrastructure as Code tool
- [sky](https://skypilot.readthedocs.io/en/latest/getting-started/installation.html) - Cloud management tool
- [civo](https://www.civo.com/learn/how-to-install-civo-cli) - Civo CLI
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) - Kubernetes CLI

## Setup Instructions

### 1. Repository Setup

You have two options for setting up the repository:

#### Option A: Clone the Complete LMOrBits Repository

```bash
gh repo clone LMOrBits/lmorbits
cd lmorbits
```

#### Option B: Clone Infrastructure Repository Separately

```bash
gh repo clone LMOrBits/slmops_infra
mv slmops_infra infrastructure
```

### 2. Install Taskfile

Choose one of the following installation methods:

#### Local Python Installation

```bash
cd infrastructure
uv sync
source .venv/bin/activate
```

#### Direct Taskfile Installation

Install via [taskfile website](https://taskfile.dev/installation/)

### 3. Google Cloud Authentication

```bash
gcloud auth login
```

### 4. Civo API Configuration

1. Create a Civo account if you don't have one: [Signup here](https://www.civo.com/signup)
2. Generate an API key following the [official guide](https://www.civo.com/docs/account/api-keys)
3. Set your API key:

```bash
echo export TF_VAR_civo_token=<your-civo-api-key> > cloud/terraform/environments/dev/.env
```

### 5. Cluster Configuration

Edit your cluster configuration:

```bash
code cloud/terraform/environments/dev/civo-cluster-config.yaml
```

#### Available Cluster Sizes

| Name            | Description                 | Type       | CPU Cores | RAM MB | SSD GB | Selectable |
| --------------- | --------------------------- | ---------- | --------- | ------ | ------ | ---------- |
| g4s.kube.xsmall | Extra Small - Standard      | Kubernetes | 1         | 1024   | 30     | Yes        |
| g4s.kube.small  | Small - Standard            | Kubernetes | 1         | 2048   | 40     | Yes        |
| g4s.kube.medium | Medium - Standard           | Kubernetes | 2         | 4096   | 50     | Yes        |
| g4s.kube.large  | Large - Standard            | Kubernetes | 4         | 8192   | 60     | Yes        |
| g4p.kube.small  | Small - Performance         | Kubernetes | 4         | 16384  | 60     | Yes        |
| g4p.kube.medium | Medium - Performance        | Kubernetes | 8         | 32768  | 80     | Yes        |
| g4p.kube.large  | Large - Performance         | Kubernetes | 16        | 65536  | 120    | Yes        |
| g4p.kube.xlarge | Extra Large - Performance   | Kubernetes | 32        | 131072 | 180    | Yes        |
| g4c.kube.small  | Small - CPU optimized       | Kubernetes | 8         | 16384  | 60     | Yes        |
| g4c.kube.medium | Medium - CPU optimized      | Kubernetes | 16        | 32768  | 80     | Yes        |
| g4c.kube.large  | Large - CPU optimized       | Kubernetes | 32        | 65536  | 120    | Yes        |
| g4c.kube.xlarge | Extra Large - CPU optimized | Kubernetes | 64        | 131072 | 180    | Yes        |
| g4m.kube.small  | Small - RAM optimized       | Kubernetes | 2         | 16384  | 60     | Yes        |
| g4m.kube.medium | Medium - RAM optimized      | Kubernetes | 4         | 32768  | 80     | Yes        |
| g4m.kube.large  | Large - RAM optimized       | Kubernetes | 8         | 65536  | 120    | Yes        |
| g4m.kube.xlarge | Extra Large - RAM optimized | Kubernetes | 16        | 131072 | 180    | Yes        |

### 6. Infrastructure Deployment

```bash
task cloud:initiate-iac
```

When prompted, enter `dev` as the environment name.

> ⚠️ **Important**: Review the Terraform plan carefully before confirming with `yes`.

### 7. Kubernetes Configuration

Set up kubectl context:

```bash
source <(uv run task cloud:iac:activate-kubeconfig)
```

Alternative manual setup:

```bash
cp cloud/terraform/environments/dev/keys /tmp/kubeconfig-dev
export KUBECONFIG=/tmp/kubeconfig-dev
```

Verify cluster access:

```bash
kubectl get nodes
```

### 8. Package Installation

Install required packages:

```bash
task cloud:initiate-k8s
```

Monitor deployment:

```bash
uv run watch
```

### 9. Domain Configuration

1. Get ingress IP:

```bash
uv run task cloud:k8s:get-ingress-ip
```

2. Update domain settings:

```bash
uv run task cloud:k8s:change-main-domain PREVIOUS_DOMAIN=lmorbits.com NEW_DOMAIN=custom.com
```

3. Configure DNS records as shown:
   ![DNS Configuration Example](./dns.png)

### 10. Service Access

Access your services through the configured domain. Initial credentials:

- MLFlow: See [mlflow configuration](../../../infrastructure/cloud/manifests/mlflow.yml)
- LakeFS and ZenML: Set credentials on first login

🎉 **Congratulations! Your infrastructure is now ready.**

## Maintenance and Cleanup

### Removing Resources

#### Option 1: Complete Cleanup

```bash
task cloud:delete-k8s
task cloud:delete-dev-environment
```

#### Option 2: Cluster Management

To disable Civo cluster:

```bash
sed -i '' 's/enable_civo_cluster = true/enable_civo_cluster = false/g' \
  cloud/terraform/environments/dev/terraform.tfvars
```

To re-enable Civo cluster:

```bash
sed -i '' 's/enable_civo_cluster = false/enable_civo_cluster = true/g' \
  cloud/terraform/environments/dev/terraform.tfvars
```

> 📝 **Note**: If encountering volume deletion errors, manually remove them from the Civo dashboard before retrying.
