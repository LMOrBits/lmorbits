import argparse
from mlflow import MlflowClient
import os
import mlflow
from mlflow.pyfunc.model import PythonModel
from ml.experiment.hugging_face.pull import download_model_artifact

from pathlib import Path

class LlamaGGUFWrapper(PythonModel):
    def load_context(self, context):
        pass

    def predict(self, context, model_input):
        return model_input
      


if __name__ == "__main__":   
    args = argparse.ArgumentParser()
    args.add_argument("--model_name", type=str, required=True)
    args.add_argument("--model_registry_name", type=str, required=True)
    args.add_argument("--model_name_path", type=str, required=False)
    # args.add_argument("--repo_id", type=str, required=True)
    # args.add_argument("--model_url", type=str, required=True)
    args = args.parse_args()
    print(args)
    here = Path(__file__).parent
    model_name = args.model_name
    model_name_path = model_name.replace("/", "_")
    desired_path = here/ "models"
    desired_path.mkdir(exist_ok=True, parents=True)
    desired_path = desired_path / model_name_path

    model_name_path = args.model_name_path if args.model_name_path.endswith(".gguf") else None
    download_model_artifact(args.model_name,desired_path, model_name_path=model_name_path)
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

    client = MlflowClient(tracking_uri)
    os.environ["MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD"] = "true"

    # For example, use a 50 MB threshold: if file size >= 50 MB, use multipart upload.
    os.environ["MLFLOW_MULTIPART_UPLOAD_MINIMUM_FILE_SIZE"] = str(50 * 1024 * 1024)
    # Set chunk size to 10 MB (adjust based on your network/storage performance).
    os.environ["MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE"] = str(10 * 1024 * 1024)
    
    # Path to your GGUF model
    model_save_path = f"{desired_path}/model_path/artifacts"
    
    # Start an MLflow run
    with mlflow.start_run() as run:
        # Log the custom model
        mlflow.pyfunc.log_model(
            artifact_path="model_path",
            python_model=LlamaGGUFWrapper(),
            artifacts={
                "model_path": f"{model_save_path}/model.gguf"
            },
            pip_requirements=[
                "mlflow==2.4.0",
                "llama-cpp-python",
                "pandas"
            ]
        )
        model_uri = f"runs:/{run.info.run_id}/model"
        model_details = mlflow.register_model(
            model_uri=model_uri, name=args.model_registry_name
        )
        client.update_model_version(
            name=args.model_registry_name,
            version=model_details.version,
            description=f"hf model from {args.model_name} converted to mlflow model"
        )