from data.utils.lakefs import DatasetType, LakeFSCredentials, LakeFsDataset
from zenml.client import Client
from zenml import log_metadata

def get_lakefs_credentials() -> LakeFSCredentials:
    secret = Client().get_secret("lakefs_credentials")
    credentials = LakeFSCredentials(
        endpoint_url=secret.secret_values["LAKECTL_SERVER_ENDPOINT_URL"],
        access_key_id=secret.secret_values["LAKECTL_CREDENTIALS_ACCESS_KEY_ID"],
        secret_access_key=secret.secret_values["LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY"],
        namespace=secret.secret_values["LAKECTL_NAMESPACE"],
    )
    return credentials

def get_lakefs_dataset( directory: str, project_name: str, dataset_type:str="raw") -> LakeFsDataset:
    credentials = get_lakefs_credentials()
    lakefs_dataset = LakeFsDataset(
        credentials=credentials,
        dataset_type=DatasetType(dataset_type),
        directory=directory,
        project_name=project_name,
    )
    return lakefs_dataset

def log_lakefs_dataset(lakefs_dataset: LakeFsDataset):
    log_metadata(
        metadata={
            "lakefs_info":{
                "namespace":lakefs_dataset.credentials.namespace,
                "repo_name":lakefs_dataset.lakefs_client.repo_manager.repo_name,
                "branch_name":lakefs_dataset.lakefs_client.branch_manager.current_branch,
                "address":lakefs_dataset.credentials.endpoint_url + "/repositories/"
                + lakefs_dataset.lakefs_client.repo_manager.repo_name
                + "/objects?ref=main&path="
                + lakefs_dataset.dataset.get_path()
            }
        }
    )