from orchestration.dev.steps.ml.embeding.push_model import push_model
from zenml import pipeline

from orchestration.cli.pipe import dev,click

from orchestration.utils.config import run_or_modify_config 

@pipeline()
def push_model_embedding_pipeline(
  model_name: str,
) -> None:
  push_model(model_name=model_name)

@dev.command()
@click.option("--config", is_flag=True, help="Modify the config file")
def push_model_embedding(config:bool):
  """
  ----
  Pipeline that pushes the model to the MLflow server.
  ----
  """
  run_or_modify_config(
    "dev/ml/embedding/push_model_embedding.yaml",
    push_model_embedding_pipeline,
    config=config
  )