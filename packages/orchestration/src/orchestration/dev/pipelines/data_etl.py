from pathlib import Path
from typing import Any, Dict, List, Optional

from data.utils.hugging_face import get_info
from loguru import logger
from omegaconf import OmegaConf
from zenml import log_metadata, pipeline

from orchestration.dev.steps.etl.data_ingestion_hf_to_lakefs import (
    Splits,
    etl_from_hf_to_lakefs,
)


@pipeline
def data_etl_pipeline(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    splits: List[Dict[str, Any]],
    config: Optional[str] = None,
) -> List[str] | None:
    logger.info(f"Ingesting dataset {hf_dataset_name} into {project_name}/{directory}")
    splits= Splits(splits=splits)
    
    addresses = etl_from_hf_to_lakefs(hf_dataset_name, project_name, directory, splits)
    return addresses


def main():
    ocrchestration_dir = Path(__file__).parents[4]
    config_path = ocrchestration_dir / "configs/dev/data.yaml"
    cfg = OmegaConf.load(config_path)
    dataetl_pipeline_configured = data_etl_pipeline.with_options(**OmegaConf.to_container(cfg))
    dataetl_pipeline_configured()


if __name__ == "__main__":
    main()
