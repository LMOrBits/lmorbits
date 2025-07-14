from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Tuple

from data.utils.hugging_face import get_info, get_one_sample
from loguru import logger
from omegaconf import OmegaConf
from zenml import log_metadata, pipeline
from zenml.types import HTMLString

from orchestration.dev.steps.etl.data_ingestion_hf_to_lakefs import (
    Split,
    etl_from_hf_to_lakefs_step,
)
from orchestration.utils.tables import display_dict_of_tables


@pipeline(enable_cache=False)
def data_etl_pipeline(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    splits: List[Split],
    config: Optional[str] = None,
) -> Annotated[dict, "address_dict"]:
    logger.info(f"Ingesting dataset {hf_dataset_name} into {project_name}/{directory}")
    address_dict = {}
    for split in splits:
        address_dict[split.name] = etl_from_hf_to_lakefs_step(hf_dataset_name, project_name, directory, split, config)
    return address_dict


def main():
    ocrchestration_dir = Path(__file__).parents[4]
    config_path = ocrchestration_dir / "configs/dev/data.yaml"
    cfg = OmegaConf.load(config_path)
    dataetl_pipeline_configured = data_etl_pipeline.with_options(**OmegaConf.to_container(cfg))
    dataetl_pipeline_configured()


if __name__ == "__main__":
    main()
