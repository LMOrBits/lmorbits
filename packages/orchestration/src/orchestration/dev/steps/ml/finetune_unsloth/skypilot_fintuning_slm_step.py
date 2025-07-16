
from zenml import pipeline, step, log_metadata
from orchestration.utils.skypilot import (
    zenml_orchestration_run_skypilot_task,
    prettify_task_config,
)
from typing import Dict, Any
from pathlib import Path


@step
def sky_finetuning_slm(sky_config: Dict[str, Any]):
    log_metadata(metadata={"sky_config": prettify_task_config(sky_config)})
    zenml_orchestration_run_skypilot_task(task_config=sky_config)





