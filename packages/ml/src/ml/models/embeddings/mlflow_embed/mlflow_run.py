from mlflow import MlflowClient
from dotenv import load_dotenv
import os
import mlflow
from mlflow.pyfunc.model import PythonModel
import argparse
# from ml.cli.group import embedding, click

# load_dotenv()

class RAGEmbeddingsModel(PythonModel):
    def load_context(self, context):
        # Load any model artifacts here
        pass

    def predict(self, context, model_input):
        # Implement your prediction logic here
        return model_input



# @embedding.command()
# @click.option("--model_name", type=str, required=True)
# def push_model(model_name: str):

#     client = MlflowClient(os.getenv("MLFLOW_TRACKING_URI"))

#     model_name = "airplane_simple_retriever_embeddings"
    
#     print("initiating mlflow run , tracking uri: ", os.getenv("MLFLOW_TRACKING_URI"))
#     with mlflow.start_run() as run:
#         print("mlflow run initiated")

#         mlflow.log_artifacts("serve", "serve")
#         model_uri = f"runs:/{run.info.run_id}/model"
#         model_details = mlflow.register_model(
#             model_uri=model_uri, name=model_name
#         )
#         client.update_model_version(
#             name=model_name,
#             version=model_details.version,
#             description="Test model version"
#         )
#         model_versions = client.search_model_versions(f"name='{model_name}'")
#         click.echo(f"Model {model_name} pushed to mlflow")

    
if __name__ == "__main__":
    client = MlflowClient(os.getenv("MLFLOW_TRACKING_URI"))
    args = argparse.ArgumentParser()
    args.add_argument("--model_name", type=str, required=True)

    args = args.parse_args()

    model_name = args.model_name or "airplane_simple_retriever_embeddings"
    
    print("initiating mlflow run , tracking uri: ", os.getenv("MLFLOW_TRACKING_URI"))
    with mlflow.start_run() as run:
        print("mlflow run initiated")

        mlflow.log_artifacts("serve", "serve")
        model_uri = f"runs:/{run.info.run_id}/model"
        model_details = mlflow.register_model(
            model_uri=model_uri, name=model_name
        )
        client.update_model_version(
            name=model_name,
            version=model_details.version,
            description="Test model version"
        )
        model_versions = client.search_model_versions(f"name='{model_name}'")
