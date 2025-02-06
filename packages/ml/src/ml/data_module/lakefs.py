from ml.config import config
from data.utils.lakefs import LakeFSCredentials
from data.utils.lakefs import LakeFsDataset,DatasetType
from datasets import load_dataset
def get_dataset(
    directory: str,
    project_name: str,
    dataset_type: str = "bronze",
    branch_name: str = "main",
    split: str = "train",
    num_proc: int = 2,
):
  config()
  credentials = LakeFSCredentials.from_env()
  lakefs_dataset = LakeFsDataset(credentials=credentials,
                               dataset_type=DatasetType(dataset_type), 
                               directory=directory, 
                               project_name=project_name, 
                              )

  data_files = lakefs_dataset.load_data_files()
  dataset = load_dataset("parquet", data_files=data_files , split=split, num_proc=num_proc)
  return dataset