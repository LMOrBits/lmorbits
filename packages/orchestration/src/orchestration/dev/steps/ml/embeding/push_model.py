from ml.task import push_embedding
from zenml import log_metadata, step


@step
def push_model(
  model_name: str,
) -> None:
  """
  Push the model to the MLflow server.
  """
  push_embedding(model_name)