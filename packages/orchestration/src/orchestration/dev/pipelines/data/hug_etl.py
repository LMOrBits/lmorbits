from typing import Annotated, Dict, List

from loguru import logger
from zenml import  pipeline

from orchestration.dev.steps.data.etl.data_ingestion_hf_to_lakefs import (
    LakefsInfo,
    Split,
    etl_from_hf_to_lakefs_step,
)
from orchestration.cli.pipe import dev,click
from orchestration.utils.config import run_or_modify_config



@pipeline(enable_cache=False)
def hug_etl_pipeline(
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




@dev.command()
@click.option("--config", is_flag=True, help="Modify the config file")
def hug_etl(config:bool):
    """
    ----
    Pipeline that performs ETL operations on Hugging Face datasets:
    1. Extracts data from Hugging Face
    2. Transforms and loads it to LakeFS

    The pipeline configuration is read from dev/data.yaml
    ----
    """
    run_or_modify_config("dev/data/hug_etl.yaml", hug_etl_pipeline, config=config)
