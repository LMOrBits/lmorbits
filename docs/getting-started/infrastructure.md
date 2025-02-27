---
icon: cloud
description: Learn how to develop applications with our ML platform
---

# Infrastructure

In this section, we will explore the ecosystem and platform used for orchestration. We can categorize our approach into two main types: local and cloud environments.

For the local environment, we will utilize K3D or K3S to manage a local Kubernetes setup. On the other hand, for the cloud environment, we will adopt Terraform for our Infrastructure as Code (IaC) strategy, primarily focusing on Google Cloud (gcloud).

In the following sections, we will delve deeper into the necessary components and implementations for the Kubernetes system.


## Local Environment / (on-prem)

For a local environment, it is recommended to have a proper GPU instance in your K3S setup (on-prem) or run K3d on a GPU if you require GPU capabilities. Other than that, no additional components are necessary for a local environment, as all packages are managed via cloud alternatives like MinIO for S3 storage.

## Cloud Environment

For a cloud environment, the most crucial step is to ensure that you have properly initiated gcloud in your terminal. The primary components we will use include artifact registry, storage registry, and storage blobs. For compute resources, we will utilize SkyPilot and CIVO for Kubernetes, or alternatively, GKS can also be used as a Kubernetes ecosystem. In summary, you will need to enable artifact registry, storage, and GPU access.