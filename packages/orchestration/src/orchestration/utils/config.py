from pathlib import Path
from omegaconf import OmegaConf
from typing import Callable


def modify_config(config_relative_path: str):
    import subprocess
    subprocess.run(["vim", config_relative_path])

def run_pipeline(config_path: str, pipeline_function: Callable):
    cfg = OmegaConf.load(config_path)
    pipeline_function = pipeline_function.with_options(**OmegaConf.to_container(cfg))
    pipeline_function()

def run_or_modify_config(config_relative_path: str, pipeline_function: Callable , config:bool=False):
    orchestration_dir = Path(__file__).parents[3]
    config_path = orchestration_dir / "configs" / config_relative_path
    if config:
        modify_config(config_path)
    else:
        run_pipeline(config_path, pipeline_function)