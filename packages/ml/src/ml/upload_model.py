import serve.mlflow.config as config
import mlflow
import os
from llamacpp import LlamaCppModel
from loguru import logger


def llamacpp_model_register(run, model_registry_name: str):
    mlflow.pyfunc.log_model(
        artifact_path="model_path",
        python_model=LlamaCppModel(),
        artifacts={"model_path": "model.gguf"},
        pip_requirements=["mlflow==2.4.0", "llama-cpp-python", "pandas"],
    )
    run_id = run.info.run_id
    model_uri = f"runs:/{run_id}/model"
    logger.info(f"Model logged at URI: {model_uri}")
    model_details = mlflow.register_model(model_uri=model_uri, name=model_registry_name)
    logger.info(
        f"Registered model '{model_details.name}' with version {model_details.version}"
    )


def main():
    mlflow_config = config.config_init()
    mlflow.set_tracking_uri(mlflow_config["mlflow"]["URL"])
    enable_multipart_upload()
    mlflow.set_experiment("model_test")
    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            artifact_path="model_path",
            python_model=LlamaCppModel(),
            artifacts={"model_path": "model.gguf"},
            pip_requirements=["mlflow==2.4.0", "llama-cpp-python", "pandas"],
        )
        run_id = run.info.run_id
        model_uri = f"runs:/{run_id}/model"
        logger.info(f"Model logged at URI: {model_uri}")
        registered_model_name = "qa_model"
        model_details = mlflow.register_model(
            model_uri=model_uri, name=registered_model_name
        )
        logger.info(
            f"Registered model '{model_details.name}' with version {model_details.version}"
        )


if __name__ == "__main__":
    main()
