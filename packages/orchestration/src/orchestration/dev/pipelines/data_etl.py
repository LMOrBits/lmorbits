from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Tuple

from data.utils.hugging_face import get_info, get_one_sample
from loguru import logger
from omegaconf import OmegaConf
from zenml import log_metadata, pipeline
from zenml.types import HTMLString

from orchestration.dev.steps.etl.data_ingestion_hf_to_lakefs import (
    LakefsInfo,
    Split,
    etl_from_hf_to_lakefs_step,
)
from orchestration.dev.steps.etl.preprocessing import bronze_pipeline_step


@pipeline(enable_cache=False)
def data_etl_pipeline(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    splits: List[Split],
    config: str,
) -> Annotated[Dict[str, LakefsInfo], "lakefs_info_dict"]:
    logger.info(f"Ingesting dataset {hf_dataset_name} into {project_name}/{directory}")
    address_dict = {}
    for split in splits:
        address_dict[split.name] = etl_from_hf_to_lakefs_step(hf_dataset_name, project_name, directory, split, config)
    return address_dict

@pipeline(enable_cache=False)
def data_pipeline(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    splits: List[Split],
    config: str,
) -> Annotated[dict, "address_dict"]:
    ## etl process:
    adresses = data_etl_pipeline(hf_dataset_name, project_name, directory, splits, config)
    for split_name, lakefs_info in adresses.items():
        bronze_pipeline_step(lakefs_info, split_name)
    return {}

def main():
    ocrchestration_dir = Path(__file__).parents[4]
    config_path = ocrchestration_dir / "configs/dev/data.yaml"
    cfg = OmegaConf.load(config_path)
    dataetl_pipeline_configured = data_pipeline.with_options(**OmegaConf.to_container(cfg))
    dataetl_pipeline_configured()


if __name__ == "__main__":
    main()
