from zenml import pipeline, step, log_metadata
from orchestration.utils.skypilot import (
    zenml_orchestration_run_skypilot_task,
    prettify_task_config,
)
from typing import Dict, Any
from pathlib import Path


@step
def test_sky_simple(sky_config: Dict[str, Any]):
    log_metadata(metadata={"sky_config": prettify_task_config(sky_config)})
    zenml_orchestration_run_skypilot_task(task_config=sky_config)


@pipeline
def test_sky_simple_pipeline():
    test_sky_simple()


if __name__ == "__main__":
    test_sky_simple_pipeline.with_options(config_path=Path(f"{__file__}").parent / "configs/simple_sky.yaml")()
