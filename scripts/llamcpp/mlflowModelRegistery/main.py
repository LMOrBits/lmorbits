import config
import mlflow
import os 
from llamacpp import LlamaCppModel

def main():
    mlflow_config = config.config_init()
    mlflow.set_tracking_uri(mlflow_config['mlflow']['URL'])
    os.environ["MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD"] = "true"
    # For example, use a 50 MB threshold: if file size >= 50 MB, use multipart upload.
    os.environ["MLFLOW_MULTIPART_UPLOAD_MINIMUM_FILE_SIZE"] = str(50 * 1024 * 1024)
    # Set chunk size to 10 MB (adjust based on your network/storage performance).
    os.environ["MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE"] = str(10 * 1024 * 1024)
    mlflow.set_experiment("model_test")
    with mlflow.start_run() as run:
      mlflow.pyfunc.log_model(
          artifact_path="model_path",
          python_model=LlamaCppModel(),
          artifacts={"model_path": "model.gguf"},
          pip_requirements=[
              "mlflow==2.4.0",      # adjust to your desired version
              "llama-cpp-python",    # ensure this package is available on PyPI
              "pandas"
          ]
      )
      run_id = run.info.run_id
      model_uri = f"runs:/{run_id}/model"
      print(f"Model logged at URI: {model_uri}")
    registered_model_name = "qa_model"
    model_details = mlflow.register_model(model_uri=model_uri, name=registered_model_name)
    print(f"Registered model '{model_details.name}' with version {model_details.version}")

if __name__ == "__main__":
    main()