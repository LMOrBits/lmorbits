.PHONY: delete-test-pipelines delete-dev-pipelines
-include ../../.env

data-zen-integrations:
	uv run zenml integration install --uv kubernetes -y
	uv run zenml integration install --uv gcp -y
	uv run zenml integration install --uv mlflow -y
	uv run zenml integration install --uv skypilot_gcp -y

init-data: 
	uv sync --only-group data-package
	$(MAKE) data-zen-integrations




login:
	uv run zenml login $(zenml_host)


sky:
	uv run zenml stack set stack-sky-gcs

k8s:
	uv run zenml stack set stack-k8s-gcs