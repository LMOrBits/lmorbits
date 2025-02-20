from typing import Optional

from data.utils.lakefs import DatasetType, LakeFSCredentials, LakeFsDataset
from datasets import load_dataset,Dataset

from ml.config import config


def get_dataset(
    directory: str,
    project_name: str,
    dataset_type: str = "bronze",
    branch_name: str = "main",
    split: str = "train",
    num_proc: int = 2,
) -> Dataset:
    config()
    return get_dataset_from_lakefs(
        directory=directory,
        project_name=project_name,
        dataset_type=dataset_type,
        branch_name=branch_name,
        split=split,
        num_proc=num_proc,
    )

def get_dataset_from_lakefs(
    directory: str,
    project_name: str,
    dataset_type: str = "bronze",
    branch_name: str = "main",
    split: str = "train",
    num_proc: int = 2,
    lakefs_credentials: Optional[LakeFSCredentials] = None,
) -> Dataset:
    if lakefs_credentials is None:
        lakefs_credentials = LakeFSCredentials.from_env()
    lakefs_dataset = LakeFsDataset(
        credentials=lakefs_credentials,
        dataset_type=DatasetType(dataset_type),
        directory=directory,
        project_name=project_name,
        branch_name=branch_name,
    )

    data_files = lakefs_dataset.load_data_files()
    dataset = load_dataset(
        "parquet", data_files=data_files, split=split, num_proc=num_proc
    )
    return dataset
