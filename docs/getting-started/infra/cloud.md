---
icon: cloud
description: Learn how to develop applications with our ML platform
---

# prerequisites

- [gcloud](https://cloud.google.com/sdk/docs/install)
- [terraform](https://www.terraform.io/downloads)
- [sky](https://skypilot.readthedocs.io/en/latest/getting-started/installation.html)
- [civo](https://www.civo.com/learn/how-to-install-civo-cli)

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

7. now after this you will be able to see the new configs in the
