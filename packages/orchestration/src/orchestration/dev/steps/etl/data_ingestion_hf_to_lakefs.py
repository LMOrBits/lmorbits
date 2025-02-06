from zenml.client import Client
from pydantic import BaseModel
from loguru import logger
from typing_extensions import Annotated, Literal 
from zenml import get_step_context, step,log_metadata
from data.etl.hf_to_lakefs import stream_and_upload_from_hf_to_lakefs
from data.utils.lakefs import LakeFSCredentials, LakeFsDataset, DatasetType
from typing import Optional

class Split(BaseModel):
    name: str 
    chunk_size: int = 2000
    start: Optional[int]=None
    end: Optional[int]=None

@step
def etl_from_hf_to_lakefs(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    split: Split,
)-> Annotated[dict, "address_dict"]:

  logger.info(f"Ingesting dataset {hf_dataset_name} into {project_name}/{directory}")
  logger.info(f"split: {split}")
  secret = Client().get_secret("lakefs_credentials")
  credentials = LakeFSCredentials(
    endpoint_url=secret.secret_values["LAKECTL_SERVER_ENDPOINT_URL"],
    access_key_id=secret.secret_values["LAKECTL_CREDENTIALS_ACCESS_KEY_ID"],
    secret_access_key=secret.secret_values["LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY"],
    namespace=secret.secret_values["LAKECTL_NAMESPACE"]
  )

  lakefs_dataset = LakeFsDataset(
                               credentials=credentials,
                               dataset_type=DatasetType("raw"), 
                               directory=directory, 
                               project_name=project_name, 
                              )
  
  address_dict = stream_and_upload_from_hf_to_lakefs(hf_dataset_name, lakefs_dataset, chunk_size= split.chunk_size, start= split.start, end= split.end)
  log_metadata(
    metadata={
        "dataset_info": {
              "hf_dataset_name": hf_dataset_name,
              "project_name": project_name,
              "directory": directory,
              "split": split.name,
              "chunk_size": split.chunk_size,
              "start": split.start,
              "end": split.end
          },
        "lakefs_info": {
              "dataset_type": "raw",
              "ml_dataset_type": split.name,
              "namespace": lakefs_dataset.credentials.namespace,
              "repo_name": lakefs_dataset.lakefs_client.repo_manager.repo_name,
              "branch_name": lakefs_dataset.lakefs_client.branch_manager.current_branch,
              "address":  lakefs_dataset.credentials.endpoint_url + "/repositories/" + lakefs_dataset.lakefs_client.repo_manager.repo_name + "/objects?ref=main&path=" +lakefs_dataset.dataset.get_path() 
          }
      }
  )

  return address_dict



