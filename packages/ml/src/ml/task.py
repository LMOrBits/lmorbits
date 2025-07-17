from taskpy import TaskCLI
from pathlib import Path
from dotenv import load_dotenv
import os

ml_repo_dir = Path(__file__).parents[2]
ml_repo_task = TaskCLI(ml_repo_dir)
emmbedding_task = TaskCLI(ml_repo_dir/"src/ml/models/embeddings/mlflow_embed")


def push_embedding(model_name:str):
    """
    Push the embedding to the MLflow server.
    """
    os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_ADDRESS" )
    os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_USERNAME")
    os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_PASSWORD")
    emmbedding_task.run("push", MODEL_NAME=model_name)

if __name__ == "__main__":
    load_dotenv(ml_repo_dir / ".env")
    push_embedding()










