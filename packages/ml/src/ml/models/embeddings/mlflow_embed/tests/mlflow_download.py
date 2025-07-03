from mlflow import MlflowClient
from dotenv import load_dotenv
import os
from mlflow.pyfunc import PythonModel
from pathlib import Path
from mlflow.artifacts import download_artifacts

load_dotenv("../.env")

class RAGEmbeddingsModel(PythonModel):
    def load_context(self, context):
        # Load any model artifacts here
        pass

    def predict(self, context, model_input):
        # Implement your prediction logic here
        return model_input
      
client = MlflowClient(os.getenv("MLFLOW_TRACKING_URI"))
model_name = "rag_embeddings"

if __name__ == "__main__":   

    model_versions = client.search_model_versions(f"name='{model_name}'")
    latest_version = max(int(mv.version) for mv in model_versions)
    model_version = client.get_model_version(model_name, str(latest_version))
    # Create a unique directory for this model version
    model_save_dir = Path(__file__).parent / f"{model_name}"
    model_save_dir.mkdir(exist_ok=True)
    
    # Download the model
    download_artifacts(
        run_id=model_version.run_id,
        artifact_path="serve",
        dst_path=str(model_save_dir)
    )

    

