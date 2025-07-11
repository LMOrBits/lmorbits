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

## 1. clone the the infrastructure repository seperately if you only want to seperate your infra repo from lmobits repo since the lmobits repo is a monorepo and the infra repo is a submodule.

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

## 2. install the taskfile

- locally via python pacakges
  ```bash
    cd infrastructure
    uv sync
    source .venv/bin/activate
  ```
- install the taskfile via [taskfile](https://taskfile.dev/installation/)

## 3. login to the gcloud :

```bash
gcloud auth login
```

## 4. put your civo api key in the .env file in dev folder

in order to get the civo api key, you first need to have a civo account.

- if you don't have a civo account, you can create one [here](https://www.civo.com/signup)
- if you have a civo account, you need to follow the steps in [here](https://www.civo.com/docs/account/api-keys) to get the api key.

```bash
echo export TF_VAR_civo_token=<your-civo-api-key> > cloud/terraform/environments/dev/.env
```

## 5. edit the desired state for the civo cluster :

```bash
code cloud/terraform/environments/dev/civo-cluster-config.yaml
```

> you can get more deatial with `civo kubernetes size` command. to get all of the sizes.

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

you can use `vim` or `nano` to edit the file.

## 6. now you can run the following command to initiate the infrastructure:

```bash
task cloud:initiate-iac
```

enter the dev when you asked to select the environment.
Environment name (e.g., dev, prod)

Enter a value: `dev`

in last step, it will show you the actions that terraform will take. please review the actions and enter `yes` to continue.

this will take a while to complete. have a cup of coffee and come back later ☕️.

> It is worth mentioning that when updating a Civo cluster using Terraform, any changes to the cluster configuration will result in the destruction and recreation of the cluster, rather than an in-place update. Please ensure you have backed up any important data before scaling or modifying the cluster configuration. please check the last section of the document to see how to delete or modify the cluster.

## 7. change the kubectl context to the new cluster:

```bash
source <(uv run task cloud:iac:activate-kubeconfig)
```

or do it manually:

```bash
cp cloud/terraform/environments/dev/keys /tmp/kubeconfig-dev
export KUBECONFIG=/tmp/kubeconfig-dev
```

test the cluster by running the following command:

```bash
kubectl get nodes
```

## 8. now its time to install the packages in the cluster.

```bash
task cloud:initiate-k8s
```

> if did not worked try to `task cloud:delete-k8s` and try again.

try now to monitor the pods in the cluster:

```bash
uv run watch
```

## 9. since we are utilitzing the ingress we need to connect our domain to the ingress. in order to get the ip of the ingress you can run the following command:

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

## 10. now you can access the mlflow, lakefs, zenml, and the rest of the services by going to the domain you have set.

    the passwords for mlflow can be found in the [mlflow](../../../infrastructure/cloud/manifests/mlflow.yml) and the passwords for lakefs and zenml will be set at the first time you login to the services.

> congratulations 🎉 you have successfully set up the infrastructure.

![success](https://media1.tenor.com/m/HUDIU5GEuFwAAAAd/jose-mourinho-funky.gif)

# how to delete all the resources

### 1. delete the packages and the pvc in the cluster

```bash
task cloud:delete-k8s
```

if you want to only remove or change the cluster type of the civo since it does not support the change of type in the terraform, and kubernetes is one of the most expensive part, you can run the following command:

```bash
sed -i '' 's/enable_civo_cluster = true/enable_civo_cluster = false/g' \
  cloud/terraform/environments/dev/terraform.tfvars
```

and if you want to enable the civo cluster again, you can run the following command:

```bash
sed -i '' 's/enable_civo_cluster = false/enable_civo_cluster = true/g' \
  cloud/terraform/environments/dev/terraform.tfvars
```

in order to change the cluster type, you can run the following command and modify the cluster type:

```bash
code cloud/terraform/environments/dev/civo-cluster-config.yaml
```

this will take a while since deleting the pvc will take a while. if it gave error about the mlflow-sereve ignore it for now.

2. delete the infrastructure

```bash
task cloud:delete-dev-environment
```

if the civo gave you error pleas go to dashboard in the volume section and deleter the volumes there, then try again. and
