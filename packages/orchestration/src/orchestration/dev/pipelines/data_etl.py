from loguru import logger
from zenml import pipeline , log_metadata
from typing import List
from orchestration.dev.steps.etl.data_ingestion_hf_to_lakefs import etl_from_hf_to_lakefs , Split
from pathlib import Path
from omegaconf import OmegaConf
from typing import Optional
from data.utils.hugging_face import get_info

@pipeline
def data_etl_pipeline(
  hf_dataset_name: str,
  project_name: str,
  directory: str,
  splits: Optional[List[dict]] = None,
):
  logger.info(f"Ingesting dataset {hf_dataset_name} into {project_name}/{directory}")
  addresses = []
  info = get_info(hf_dataset_name)
  if splits is not None:
    valid_splits = {splits["name"]: Split(**splits) for splits in splits if splits["name"] in info.keys()}
    if valid_splits is not None:
      splits = valid_splits
    else:
     return None 
  else:
    splits = {split: Split(name=split) for split in info.keys()} 
  splits_dict = {k: v.dict() for k,v in splits.items()} 
  log_metadata(
    metadata={
      "base_info": {
      **info},
      "splits":{
      **splits_dict}
    }
    )
  for split in splits.values():
    address = etl_from_hf_to_lakefs(hf_dataset_name, project_name, directory, split)
    addresses.append(address)
  return addresses



def main():
  cfg = OmegaConf.load(Path(__file__).parent.parent / "configs" / "data_ingest.yaml")
  dataetl_pipeline_configured = data_etl_pipeline.with_options(**OmegaConf.to_container(cfg))
  dataetl_pipeline_configured()

if __name__ == "__main__":
  main()