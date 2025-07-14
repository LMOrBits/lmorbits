---
description: Learn how to develop applications with our ML platform
icon: planet-ringed
---

# SimpleExample

This example demonstrates the implementation of Small Language Model Operations (SLMOps) based on our [thesis research](https://github.com/LMOrbits/thesis). The implementation follows an iterative development approach inspired by the [SLMOps paper](https://arxiv.org).

Follow these steps to get started:

## 1. Set Up the Environment

* Configure your infrastructure environment following the [infrastructure guide](getting-started/infra/). We recommend using the cloud-based deployment option, since the local deployment is not fully supported yet for fine-tuning the model.
* Ensure all prerequisites are installed and configured properly

## 2. Set up the orchestration:

### Set up the orchestration:

the documention for the orchestration is in the [orchestration](../how-to/development/lmorbits/ORCHESTRATION/) folder. but here is a quick start guide for it to start with or simple example:

#### 1. Make sure you cloned the lmorbits reposirtory:

```bash
gh repo clone LMOrBits/lmorbits
cd lmorbits
```

***

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

***

#### 3. Set up the stacks that are required for the orchestration:

we will setup 3 stacks for the orchestration:

```bash
uv run task zenml:setup:local-gcs
uv run task zenml:setup:local-gpu-gcs
uv run task zenml:setup:all-k8s
```

***

#### 4. now is the time to test the pipeline:

```bash
uv run task zenml:test:plot
```

this will test the pipeline and plot the results. and it show you the link afterwards, if it goes well. and then you can go to the link and see the results as in the image below:&#x20;

<div data-full-width="true"><figure><img src="zen1.png" alt=""><figcaption></figcaption></figure></div>

***

#### 5. creating users for the orchestration:

now we need to create a accounts for people that would work with the orchestration or resources:

```bash
uv run task zenml:setup:create-users
```

this will create a accounts for people that would work with the orchestration or resources. and then you can use the accounts to login to the zenml server and start working with the orchestration. and then you can use the accounts to login to the zenml server and start working with the orchestration.

***

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

this will create a pipeline (e.i. test\_sky\_simple\_pipeline) in which in this pipline it will create a skypilot instance and then run a new pipeline in that instance (e.i. html\_plotly\_pipline same as test which was our intention to test the pipeline in the skypilot instance that we initiated with our piplines). As you can see in the image below , the html\_plotly\_pipline will be run in the skypilot instance as the author of it is the skypilot instance.

<div data-full-width="true"><img src="zen-sky.png" alt="image of the the zenml pipeline"></div>

***

#### 7. now we set up the lakefs instace and :

go to your lakefs address and start it by providing your name and email and get the keys from there and fill the .env.example file into a .env file in the orchestration folder. this will allow us to handle the data piplines.

***

#### 8. handle the seceret keys:

now after this we need to create secrets for our lakefs instace e in the zenml secrets manager.

```bash
uv run task zenml:secrets:create-data-secrets
```

you can also check that by

```bash
uv run task zenml:secrets:get-data-secrets
```

it can also be visible in the ui by going to the zenmlui > setting > secrets: ![image of the the zenml secrets](zen-secrets.png)

***

#### 9. now we can extract data from huggingface based on the config we defined in the orchestration/config/dev/data.yaml file. and move that data into our lakefs instace.

so first we can check which split from what dataset we want to extract, in order to fascilitate the process we can use the following command for getting to konw what splits are available for instace for the dataset named squad\_v2 in huggingface:

```bash
uv run task zenml:utils:data:get-splits HF_DATASET_NAME=squad_v2
```

the outcome would be like this:&#x20;

<div data-full-width="true"><figure><img src="splits.png" alt=""><figcaption></figcaption></figure></div>

now base on this information we can extract the amount we want to our lakefs instace. by modifying the config/dev/data.yaml file.

```bash
code orchestration/config/dev/data.yaml
```

and then we can run the following command to extract the data:

```bash
uv run task zenml:piplines:data-etl-huggingface
```

you can find the link to your lakefs repo now if you go to the meta data of each step (splits)&#x20;

<div data-full-width="true"><figure><img src="data-etl-0.png" alt=""><figcaption></figcaption></figure></div>



***
