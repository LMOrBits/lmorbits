# .PHONY: integrate-kubernetes
ifneq (,$(wildcard .env))
    include .env
    export
endif

#region Variables
mlflow_address := $(MLFLOW_ADDRESS)
mlflow_username := $(MLFLOW_USERNAME)
mlflow_password := $(MLFLOW_PASSWORD)

docker_json_key := $(shell cat $(DOCKER_JSON_PATH))

docker_email := $(DOCKER_EMAIL)
docker_server := $(DOCKER_SERVER)

gcs_project_id := $(GCS_PROJECT_ID)
gcs_bucket_name_ml_artifacts := $(GCS_BUCKET_NAME_ML_ARTIFACTS)
gcs_bucket_name_data := $(GCS_BUCKET_NAME_DATA)
gcs_registry_repo_name := $(GCS_REGISTRY_REPO_NAME)
gcs_region := $(GCS_REGION)
sky_service_account_json_path := $(shell cat $(SKY_SERVICE_ACCOUNT_JSON_PATH))
ml_dev_user_name := $(or $(ML_DEV_USER_NAME),"ML_DEV")
ml_dev_user_password := $(or $(ML_DEV_USER_PASSWORD),"ML_DEV")

data_dev_user_name := $(or $(DATA_DEV_USER_NAME),"DATA_DEV")
data_dev_user_password := $(or $(DATA_DEV_USER_PASSWORD),"DATA_DEV")

serve_user_name := $(or $(SERVE_USER_NAME),"SERVE")
serve_user_password := $(or $(SERVE_USER_PASSWORD),"SERVE")

orchestrator_user_name := $(or $(ORCHESTRATOR_USER_NAME),"ORCHESTRATOR")
orchestrator_user_password := $(or $(ORCHESTRATOR_USER_PASSWORD),"ORCHESTRATOR")

application_user_name := $(or $(APPLICATION_USER_NAME),"APPLICATION")
application_user_password := $(or $(APPLICATION_USER_PASSWORD),"APPLICATION")

#endregion



#region Integrations


integrate-kubernetes:
	uv run zenml integration install --uv kubernetes

all-integrations:
	uv run zenml integration install --uv kubernetes -y
	uv run zenml integration install --uv gcp -y
	uv run zenml integration install --uv mlflow -y
	uv run zenml integration install --uv skypilot_gcp -y
	uv run zenml integration install --uv skypilot_kubernetes -y
#endregion

#region users
create-users:
	uv run zenml user create $(ml_dev_user_name) --password $(ml_dev_user_password) --is_admin
	uv run zenml user create $(data_dev_user_name) --password $(data_dev_user_password) --is_admin
	uv run zenml user create $(serve_user_name) --password $(serve_user_password) --is_admin
	uv run zenml user create $(orchestrator_user_name) --password $(orchestrator_user_password) --is_admin
	uv run zenml user create $(application_user_name) --password $(application_user_password)
#endregion
#region service account
create-service-account:
	uv run zenml service-account create sky-service-account
#endregion
#region all at once
# all-k3d: 
# 	create-gcs-connector ; 
# 	create-gcs-artifact-store ; 
# 	create-gcs-container-registry ; 
# 	create-k3d-orchestrator ; 
# 	create-local-image-builder ; 
# 	add-mlflow-tracking ; 
# 	add-data-validation ; 
	
local-gcs:
# @$(MAKE) create-gcs-connector
# @$(MAKE) create-gcs-artifact-store
	@$(MAKE) create-local-orchestrator
	@$(MAKE) setup-stack-local-gcs-mlflow

local-gpu-gcs:
	@$(MAKE) create-local-gpu-orchestrator
	@$(MAKE) setup-stack-local-gpu-gcs-mlflow

all-k8s: 
	@$(MAKE) all-integrations
	@$(MAKE) create-gcs-connector
	@$(MAKE) create-gcs-artifact-store
	@$(MAKE) create-gcs-container-registry
	@$(MAKE) create-k8s-orchestrator
	@$(MAKE) create-local-image-builder
	@$(MAKE) add-mlflow-tracking
	@$(MAKE) add-data-validation
	@$(MAKE) k8s-enable-gcs-container-registry
	@$(MAKE) setup-stack-gcs-mlflow-k8s-gcs
#endregion

sky-gcs:
	@$(MAKE) all-integrations
	@$(MAKE) create-gcs-connector-sky
	@$(MAKE) add-sky-gcs
	@$(MAKE) setup-stack-gcs-mlflow-sky-gcs

delete-all:
	uv run zenml stack delete test-stack
	uv run zenml model-registry delete gcs-mlflow
	uv run zenml artifact-store delete gcs_store
	uv run zenml container-registry delete gcs-container-registry
	uv run zenml orchestrator delete k8s
	uv run zenml image-builder delete docker-local
	uv run zenml experiment-tracker delete mlflow_tracker
	
#region Handling Stack
stack-default:
	uv run zenml stack set default

stack-k8s:
	uv run zenml stack set stack-k8s-gcs
#endregion

#region GCP Services

create-gcs-connector:
	uv run zenml integration install gcp -y --uv
	uv run zenml service-connector register google_cloud_connector --type gcp \
		--auto-configure \
		--project_id=$(gcs_project_id)

create-gcs-artifact-store:
	uv run zenml artifact-store register gcs_store -f gcp \
		--path=gs://$(gcs_bucket_name_ml_artifacts) \
		--authentication_secret=gcp_secret
	uv run zenml artifact-store connect gcs_store --connector google_cloud_connector

create-gcs-container-registry:
	uv run zenml container-registry register gcs-container-registry \
		--flavor=gcp \
		--uri=$(docker_server)/$(gcs_project_id)/$(gcs_registry_repo_name)
	uv run zenml container-registry connect gcs-container-registry --connector google_cloud_connector

create-gcs-connector-sky:
	@uv run zenml service-connector register google_cloud_connector_sky_service \
		--type gcp \
		--auth-method=service-account \
		--service_account_json='$(sky_service_account_json_path)' \
		--project_id=$(gcs_project_id)
#endregion

#region Orchestrator Setup
# local orchestrator setup
create-local-orchestrator:
	uv run zenml orchestrator register simple-local \
		--flavor=local
# local gpu orchestrator setup
create-local-gpu-orchestrator:
	uv run zenml orchestrator register simple-local-gpu \
		--flavor=local

# K3d Orchestrator Setup
create-k3d-orchestrator:
	uv run zenml orchestrator register k3d-orchestrator \
		--flavor=kubernetes \
		--kubernetes_context=k3d-slmops-cluster
	kubectl create namespace zenml

# K8s Orchestrator Setup
create-k8s-orchestrator:
	uv run zenml orchestrator register k8s\
		--flavor=kubernetes \
		--kubernetes_context=$$(kubectl config current-context)

# SkyPilot Integration Setup
add-sky-kube:
	uv run zenml zenml integration install skypilot_kubernete  -y --uv
	uv run zenml orchestrator register sky-kube --flavor sky_kubernetes

add-sky-gcs:
	uv add "zenml[connectors-gcp]"
	uv run zenml integration install gcp skypilot_gcp --uv -y
	uv run zenml orchestrator register sky-gcs --flavor vm_gcp
	uv run zenml orchestrator connect sky-gcs --connector google_cloud_connector_sky_service
	uv run zenml service-connector update google_cloud_connector_sky_service --generate_temporary_tokens=False	


## --= Enable GCS Container Registry =--

# K3d
k3d-enable-gcs-container-registry:
	kubectl apply -f packages/orchestration/src/orchestration/scripts/access.yaml
	kubectl patch serviceaccount default -n zenml \
  	-p '{"imagePullSecrets": [{"name": "artifact-registry-secret"}]}'
	kubectl patch serviceaccount zenml-service-account -n zenml \
  	-p '{"imagePullSecrets": [{"name": "artifact-registry-secret"}]}'
	kubectl patch serviceaccount default \
  	-p '{"imagePullSecrets": [{"name": "artifact-registry-secret"}]}'

	kubectl create secret docker-registry artifact-registry-secret --namespace zenml \
		--docker-server="$(docker_server)" \
		--docker-username="_json_key" \
		--docker-password='$(docker_json_key)' \
		--docker-email="$(docker_email)"

# K8s
k8s-enable-gcs-container-registry:
	kubectl apply -f packages/orchestration/src/orchestration/scripts/access.yaml
	kubectl patch serviceaccount default -n zenml \
  	-p '{"imagePullSecrets": [{"name": "artifact-registry-secret"}]}'
	kubectl patch serviceaccount zenml-service-account -n zenml \
  	-p '{"imagePullSecrets": [{"name": "artifact-registry-secret"}]}'
	kubectl patch serviceaccount default \
  	-p '{"imagePullSecrets": [{"name": "artifact-registry-secret"}]}'

	kubectl create secret docker-registry artifact-registry-secret --namespace zenml \
		--docker-server="$(docker_server)" \
		--docker-username="_json_key" \
		--docker-password='$(docker_json_key)' \
		--docker-email="$(docker_email)"
 #endregion

#region Image Builder Setup
create-local-image-builder:
	uv run zenml image-builder register docker-local --flavor=local
	kubectl create secret generic registry-secret \
		--from-file=.dockerconfigjson=$$HOME/.docker/config.json \
		--type=kubernetes.io/dockerconfigjson
#endregion

#region MLflow Setup
add-mlflow-tracking-local:
	uv run zenml experiment-tracker register mlflow_tracker --flavor=mlflow \
		--tracking_username=admin --tracking_password=slmops \
		--tracking_uri=http://mlflow-server-tracking.default.svc.cluster.local:5000
	uv run zenml model-registry register -f mlflow gcs-mlflow

add-mlflow-tracking:
	uv run zenml experiment-tracker register mlflow_tracker --flavor=mlflow \
		--tracking_username=$(mlflow_username) --tracking_password=$(mlflow_password) \
		--tracking_uri=$(mlflow_address)
	uv run zenml model-registry register -f mlflow gcs-mlflow

show-variables:
	echo "mlflow_address: $(mlflow_address)"
	echo "mlflow_username: $(mlflow_username)"
	echo "mlflow_password: $(mlflow_password)"
	echo "docker_server: $(docker_server)"
	echo "docker_json_key: $(docker_json_key)"
	echo "docker_email: $(docker_email)"
#endregion

#region Data Validation Setup
add-data-validation:
	uv run zenml integration install deepchecks -y --uv
	uv run zenml data-validator register deepchecks_data_validator --flavor=deepchecks


#endregion

#region Stack Configurations
setup-stack-local-gcs-mlflow:
	uv run zenml stack copy default stack-local
	uv run zenml stack update stack-local \
	--artifact-store gcs_store \
	--model_registry gcs-mlflow \
	--experiment_tracker mlflow_tracker \
	--orchestrator simple-local 

	uv run zenml stack set stack-local

setup-stack-local-gpu-gcs-mlflow:
	uv run zenml stack copy default stack-local-gpu
	uv run zenml stack update stack-local-gpu \
	--artifact-store gcs_store \
	--model_registry gcs-mlflow \
	--experiment_tracker mlflow_tracker \
	--orchestrator simple-local-gpu 

	uv run zenml stack set stack-local-gpu


setup-stack-gcs-mlflow-sky-gcs:
	uv run zenml stack register stack-sky-gcs \
	--artifact-store gcs_store \
	--orchestrator sky-gcs \
	--container_registry gcs-container-registry \
	--image_builder docker-local \
	--model_registry gcs-mlflow \
	--experiment_tracker mlflow_tracker \
	--connector google_cloud_connector_sky_service \
	--set
	uv run zenml stack set stack-sky-gcs

setup-stack-gcs-mlflow-k8s-gcs:
	uv run zenml stack register stack-k8s-gcs \
	--artifact-store gcs_store \
	--orchestrator k8s \
	--container_registry gcs-container-registry \
	--image_builder docker-local \
	--model_registry gcs-mlflow \
	--experiment_tracker mlflow_tracker \
	--set
	uv run zenml stack set stack-k8s-gcs
	uv run zenml stack list

#endregion

#region Docker Build for slmops packages

# Define variables
PROJECT_ID := $(gcs_project_id)
REGION := $(gcs_region)
REPO_NAME := $(gcs_registry_repo_name)
GP ?= "none"
TAG := latest
# BUILDPLATFORM := linux/amd64,linux/arm64
IMAGE_NAME := zenml-image-$(GP)
FULL_IMAGE_NAME := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME):$(TAG)
build-tag-push: build tag push

# Build the Docker image
build:
ifeq ($(GP), ml-package)
	docker build -f ml.Dockerfile  -t $(IMAGE_NAME):$(TAG) .
else ifeq ($(GP), orchestration)
	docker build -f orchestration.Dockerfile  -t $(IMAGE_NAME):$(TAG) .
else ifeq ($(GP), data-package)
	docker buildx build --platform $(BUILDPLATFORM) -f data.Dockerfile  -t $(IMAGE_NAME):$(TAG) .
else
	docker build --build-arg SELECTED_GROUP=$(GP) -t $(IMAGE_NAME):$(TAG) .
endif

# Tag the image for Artifact Registry
tag:
	docker tag $(IMAGE_NAME) $(FULL_IMAGE_NAME)

# Authenticate Docker with Google Artifact Registry
auth:
	gcloud auth configure-docker $(docker_server)

# Push the image to Google Artifact Registry
push: auth tag
	docker push $(FULL_IMAGE_NAME)

# Clean up local images (optional)
clean:
	docker rmi $(IMAGE_NAME):$(TAG) || true
	docker rmi $(FULL_IMAGE_NAME) || true

exec:
	docker run -it $(IMAGE_NAME) /bin/bash

sky-up:
	uv run sky launch  skypilot.yaml --name gpu-l4

sky-down:
	uv run sky down gpu-l4
#endregion
