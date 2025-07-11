---
icon: cloud
description: Learn how to develop applications with our ML platform
---

# prerequisites

- [gcloud](https://cloud.google.com/sdk/docs/install)
- [terraform](https://www.terraform.io/downloads)
- [sky](https://skypilot.readthedocs.io/en/latest/getting-started/installation.html)
- [civo](https://www.civo.com/learn/how-to-install-civo-cli)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

# setup

1. clone the the infrastructure repository seperately if you only want to seperate your infra repo from lmobits repo since the lmobits repo is a monorepo and the infra repo is a submodule.

- if you want to clone the lmorbits repo, you can use the following command:
  ```bash
  gh repo clone LMOrBits/lmorbits
  cd lmorbits
  ```
- if you want to clone the infrastructure repo, you can use the following command:
  ```bash
  gh repo clone LMOrBits/slmops_infra
  mv slmops_infra infrastructure
  ```

2. install the taskfile

- locally via python pacakges
  ```bash
    cd infrastructure
    uv sync
    source .venv/bin/activate
  ```
- install the taskfile via [taskfile](https://taskfile.dev/installation/)

3. login to the gcloud :

```bash
gcloud auth login
```

4. put your civo api key in the .env file in dev folder
   in order to get the civo api key, you first need to have a civo account.

- if you don't have a civo account, you can create one [here](https://www.civo.com/signup)
- if you have a civo account, you need to follow the steps in [here](https://www.civo.com/docs/account/api-keys) to get the api key.

```bash
echo CIVO_TOKEN=<your-civo-api-key> > cloud/terraform/environments/dev/.env
```

5. edit the desired state for the civo cluster :

```bash
code cloud/terraform/environments/dev/civo-cluster-config.yaml
```

you can use `vim` or `nano` to edit the file.

6. now you can run the following command to initiate the infrastructure:

```bash
task cloud:initiate-iac
```

enter the dev when you asked to select the environment.
Environment name (e.g., dev, prod)

Enter a value: `dev`

in last step, it will show you the actions that terraform will take. please review the actions and enter `yes` to continue.

this will take a while to complete. have a cup of coffee and come back later ☕️.

you should see the nodes in the output.

> [!IMPORTANT]
> It is worth mentioning that when updating a Civo cluster using Terraform, any changes to the cluster configuration will result in the destruction and recreation of the cluster, rather than an in-place update. Please ensure you have backed up any important data before scaling or modifying the cluster configuration.

7. change the kubectl context to the new cluster:

```bash
source <(uv run task cloud:iac:activate-kubeconfig)
```

test the cluster by running the following command:

```bash
kubectl get nodes
```

8. now its time to install the packages in the cluster.

```bash
task cloud:k8s:initiate-k8s
```

9. since we are utilitzing the ingress we need to connect our domain to the ingress. in order to get the ip of the ingress you can run the following command:

```bash
uv run task cloud:k8s:get-ingress-ip
```

now go to your domain provider and add the ip to the domain, since we have mlflow , lakefs, zenml, you need to set those

so first chanage the current domain from lmorbits to your domain.

```bash
uv run task cloud:k8s:change-main-domain PREVIOUS_DOMAIN=lmorbits.com NEW_DOMAIN=custom.com
```

now you can add the ip to the domain with A type. like the below image:

![dns example](./dns.png)

10. now you can access the mlflow, lakefs, zenml, and the rest of the services by going to the domain you have set.

> [!IMPORTANT]
> It is worth mentioning that when updating a Civo cluster using Terraform, any changes to the cluster configuration will result in the destruction and recreation of the cluster, rather than an in-place update. Please ensure you have backed up any important data before scaling or modifying the cluster configuration.
