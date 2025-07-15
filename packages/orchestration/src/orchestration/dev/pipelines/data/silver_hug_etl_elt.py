from typing import Annotated, List
from zenml import  pipeline

from orchestration.dev.steps.data.etl.data_ingestion_hf_to_lakefs import Split
from orchestration.dev.pipelines.data.hug_etl import hug_etl_pipeline

from orchestration.dev.steps.data.elt.preprocessing import silver_pipeline_step
from orchestration.cli.pipe import dev,click
from orchestration.utils.config import run_or_modify_config

@pipeline(enable_cache=False)
def silver_hug_etl_elt_pipeline(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    splits: List[Split],
    config: str,
) -> Annotated[dict, "address_dict"]:
    adresses = hug_etl_pipeline(hf_dataset_name, project_name, directory, splits, config)
    for split_name, lakefs_info in adresses.items():
        silver_pipeline_step(lakefs_info, split_name)
    return {}


@dev.command()
@click.option("--config", is_flag=True, help="Modify the config file")
def silver_hug_etl_elt(config:bool):
    """
    ----
    
    Pipeline that performs ETL and ELT operations on Hugging Face datasets:
    1. Extracts data from Hugging Face
    2. Transforms and loads it to LakeFS (ETL)
    3. Loads raw data to silver tables (ELT)

    The pipeline configuration is read from dev/silver_hug_etl_elt.yaml
    ----
    """
    run_or_modify_config("dev/data/silver_hug_etl_elt.yaml", silver_hug_etl_elt_pipeline, config=config)