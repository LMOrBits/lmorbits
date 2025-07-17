---
description: Learn how to develop applications with our ML platform
icon: planet-ringed
---

# SimpleExample

This example demonstrates the implementation of Small Language Model Operations (SLMOps) based on our [thesis research](https://github.com/LMOrbits/thesis). The implementation follows an iterative development approach inspired by the [SLMOps paper](https://arxiv.org).

Follow these steps to get started:

## 1. Set Up the Environment

- Configure your infrastructure environment following the [infrastructure guide](getting-started/infra/). We recommend using the cloud-based deployment option, since the local deployment is not fully supported yet for fine-tuning the model.
- Ensure all prerequisites are installed and configured properly

## 2. Set up the orchestration:

### Set up the orchestration:

the documention for the orchestration is in the [orchestration](../how-to/development/lmorbits/ORCHESTRATION/) folder. but here is a quick start guide for it to start with or simple example:

#### 1. Make sure you cloned the lmorbits reposirtory:

```bash
gh repo clone LMOrBits/lmorbits
cd lmorbits
```

---

#### 2. Set up the orchestration(zenml):

```bash
cd packages/orchestration
uv sync
uv run task zenml:zenml-init
```

this will authenticate you with the zenml server and set up the zenml client.

then making sure we have installed the reguired integrations for the zenml:

```bash
uv run task zenml:setup:all-integrations
```

this will install the required integrations for the zenml.

---

#### 3. Set up the stacks that are required for the orchestration:

we will setup 3 stacks for the orchestration:

```bash
uv run task zenml:setup:local-gcs
uv run task zenml:setup:local-gpu-gcs
uv run task zenml:setup:all-k8s
```

---

#### 4. now is the time to test the pipeline:

```bash
uv run task zenml:test:plot
```

this will test the pipeline and plot the results. and it show you the link afterwards, if it goes well. and then you can go to the link and see the results as in the image below:&#x20;

<div data-full-width="true"><figure><img src="zen1.png" alt=""><figcaption></figcaption></figure></div>

---

#### 5. creating users for the orchestration:

now we need to create a accounts for people that would work with the orchestration or resources:

```bash
uv run task zenml:setup:create-users
```

this will create a accounts for people that would work with the orchestration or resources. and then you can use the accounts to login to the zenml server and start working with the orchestration. and then you can use the accounts to login to the zenml server and start working with the orchestration.

---

#### 6. creating a service account for the orchestration:

one more thing to do is to create a service account for the orchestration specially to use it via skypilot when we utilizing a gpu , you can do it manually via ui in zenmlui > setting > service accounts > create service account. or via the cli:

```bash
uv run task zenml:setup:create-service-account
```

this will create a service account for the orchestration. make sure that you store the generated the api keys in the .env in the lmorbits/.env file `SKY_ZENML_STORE_API_KEY = <your_api_key>` `SKY_ZENML_STORE_URL = <your_url>`

this way from now on your skypilot instances will have access to the orchestration and resources. make sure the api has to be one line

now you can test it by :

```bash
uv run task zenml:test:skypilot
```

this will create a pipeline (e.i. test_sky_simple_pipeline) in which in this pipline it will create a skypilot instance and then run a new pipeline in that instance (e.i. html_plotly_pipline same as test which was our intention to test the pipeline in the skypilot instance that we initiated with our piplines). As you can see in the image below , the html_plotly_pipline will be run in the skypilot instance as the author of it is the skypilot instance.

<div data-full-width="true"><img src="zen-sky.png" alt="image of the the zenml pipeline"></div>

---

#### 7. now we set up the lakefs instace and :

go to your lakefs address and start it by providing your name and email and get the keys from there and fill the .env.example file into a .env file in the orchestration folder. this will allow us to handle the data piplines.

---

#### 8. handle the seceret keys:

now after this we need to create secrets for our lakefs instace e in the zenml secrets manager.

```bash
uv run task zenml:secrets:create-data-secrets
```

you can also check that by

```bash
uv run task zenml:secrets:get-data-secrets
```

it can also be visible in the ui by going to the zenmlui > setting > secrets: ![image of the the zenml secrets](./zenml-secret.png)

---

#### 9. now we can extract data from huggingface based on the config we defined in the orchestration/config/dev/data.yaml file. and move that data into our lakefs instace.

so first we can check which split from what dataset we want to extract, in order to fascilitate the process we can use the following command for getting to konw what splits are available for instace for the dataset named squad_v2 in huggingface:

```bash
uv run task zenml:utils:data:get-splits HF_DATASET_NAME=squad_v2
```

the outcome would be like this:&#x20;

<div data-full-width="true"><figure><img src="splits.png" alt=""><figcaption></figcaption></figure></div>

in order to get to know what pipelines we have in the orchestration, you can use the following command:

```bash
uv run pipe dev --help
```

the outcome would be like this:

<div data-full-width="true"><figure><img src="pipe-dev-help.png" alt=""><figcaption></figcaption></figure></div>

for instance if you want to run a pipline for huggingface etl you can use the following command:

```bash
uv run pipe dev data-etl-huggingface
```

and if you want to change the config of the pipeline you can use the following command:

```bash
uv run pipe dev data-etl-huggingface --config
```

this will open an vim editor in which you can change the config of the pipeline.

for our example we will use the following command:

```bash
uv run pipe dev silver-hug-etl-elt
```

in order to see what does this pipeline do you can use the following command:

```bash
uv run pipe dev silver-hug-etl-elt --help
```

the outcome would be like this:&#x20;

<div data-full-width="true"><figure><img src="pipe-dev-silver.png" alt=""><figcaption></figcaption></figure></div>

also you can check the zenml dashborad of cheking the outcome:

<div data-full-width="true"><figure><img src="zenml-dashboard-silver.png" alt=""><figcaption></figcaption></figure></div>

---

#### 10. now we can start to fine tune the model:

as we mentioned before we will use the skypilot instance to fine tune the model. therefor we have 2 configs for the fine tuning process. one is for the skypilot instance and the other is for the model.
the below command will give you access to change the config of the skypilot instance.

```bash
uv run pipe dev sky-finetune-slm --config
```

<div data-full-width="true"><figure><img src="sky-config.png" alt=""><figcaption></figcaption></figure></div>

which under the sky_config you can change the resources of the skypilot instance. and below is the config for the finetune process. which we will use unsloth to fine tune the model. and below you can see the hyperparameters for the finetune process. and also the dataset that will be used for the finetune process. which here we used a dataset directly from huggingface. but you can comment those and uncomment the other one to use the lakefs data if you used the pipline for etl and elt.

<div data-full-width="true"><figure><img src="fine-tune-config.png" alt=""><figcaption></figcaption></figure></div>

this will start to train the model.

you can follow up the process in the zenml dashboard that we created a pipeline that boots up a skypilot instance and then fine tunes the model in that instance.

<div data-full-width="true"><figure><img src="sky-instance-meta.png" alt=""><figcaption></figcaption></figure></div>

which undernearh of this pipeline the unsloth_finetune_slm_pipeline would be running. you can also see that in your runs that this pipeline is being triggered by skypilot and is runnign in the skypilot instance. if you click on the stack of it.

<div data-full-width="true"><figure><img src="fine-tune-pipeline.png" alt=""><figcaption></figcaption></figure></div>

here is the pipeline of the unsloth finetune process:

<div data-full-width="true"><figure><img src="unsloth-pipe.png" alt=""><figcaption></figcaption></figure></div>

we do also suppuort the pusing the model to the model registry via the ml package. you can furthure check that in the ml package. under the experiment folder.

### 11. we can also push the embedding model to the model registry via the ml package. or via the zenml pipeline. since we are not yet finetuning the embedding models we can do it easily via a task.

```bash
cd packages/orchestration
uv sync --group ml-embedding-package
uv run task zenml:setup:all-integrations
uv run pipe dev push-model-embedding
```

this will push the embedding model to the model registry. this section is not ideal yet but does the job for now. in the ideal scenario we should be able to push the model via the zenml only.

<div data-full-width="true"><figure><img src="embed.png" alt=""><figcaption></figcaption></figure></div>

as you can see we pushed the model to the mlflow.lmorbits.com with and registerd it with the name of ` airplane_simple_retriever_embeddings`

> now that we have our both models we can jump on the app stack and application

### Set up the app stack and application:

setting the app stack and starting from templates is yet another story that we will cover in the proper section when we covered the maturiry levels in detail. but here we want to show how we can have them all as an simple example for the airplane app.

in order to do this lets clone the application repo in any directory you want.

```bash
cd <your_directory>
gh repo clone LMOrbits/lmorbits-app
cd lmorbits-app
```

now we can start to set up the app stack and application.
