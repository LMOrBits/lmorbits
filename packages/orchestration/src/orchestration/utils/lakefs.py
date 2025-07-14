from data.utils.lakefs import DatasetType, LakeFSCredentials, LakeFsDataset
from zenml.client import Client


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
