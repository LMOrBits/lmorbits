import sky
from loguru import logger
import os
from typing import Dict, Any, Optional
import time
import yaml
from pathlib import Path
from dotenv import load_dotenv
from orchestration.utils.load_env import load_env

load_env()

def zenml_orchestration_run_skypilot_task(task_config:Dict[str, Any], 
                                          zenml_store_url:Optional[str]=None,
                                          zenml_store_api_key:Optional[str]=None,
                                          cluster_name:Optional[str]="skypilot-cluster", ):
    zenml_store_url = zenml_store_url if zenml_store_url else os.getenv("ZENML_STORE_URL")
    zenml_store_api_key = zenml_store_api_key if zenml_store_api_key else os.getenv("SKY_ZENML_STORE_API_KEY")
    assert zenml_store_url and zenml_store_api_key, "zenml_store_url and zenml_store_api_key must be provided or set in the environment ZENML_STORE_URL and SKY_ZENML_STORE_API_KEY"

    sky_task_config = task_config.copy()
    sky_task_config["file_mounts"] = {"/lmorbits":str(Path(__file__).parents[5])}
    zenml_login_auth= {
        "ZENML_STORE_URL": zenml_store_url,
        "ZENML_STORE_API_KEY": zenml_store_api_key,
        "ZENML_CONFIG_PATH":"./"
    }
    
    if sky_task_config.get("envs",{}):
        sky_task_config["envs"].update(**zenml_login_auth)
    else:
        sky_task_config["envs"] = zenml_login_auth

    run_skypilot_task(task_config=sky_task_config, cluster_name=cluster_name)
    


def run_skypilot_task(task_config:Dict[str, Any],cluster_name="skypilot-cluster", ):
    task = sky.Task.from_yaml_config(task_config)
    
    # Launch the task
    job_id, handle = sky.launch(
        task,
        cluster_name=cluster_name,
        # idle_minutes_to_autostop=3,
        retry_until_up=True,
        stream_logs=True,
        # down=True
        fast=True
    )

    logger.info(f"Job launched with ID: {job_id} with handle: {handle}")

    try:
        while True:
            status = sky.job_status(cluster_name=cluster_name, job_ids=[job_id])
            logger.info(f"Current job status: {status[job_id]}")
            
            if status[job_id] == sky.JobStatus.SUCCEEDED:
                logger.info("Job completed successfully")
                break
            elif status[job_id] in [sky.JobStatus.FAILED, sky.JobStatus.CANCELLED]:
                logger.error(f"Job failed or was cancelled. Status: {status[job_id]}")
                sky.down(cluster_name=cluster_name)
                return
            
            time.sleep(20)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        logger.info("Cleaning up resources...")
        sky.down(cluster_name=cluster_name)
        logger.info("Cluster resources removed")




class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)

def convert_multiline_to_list(data: dict) -> dict:

    output = {}

    for key in data.keys():  # Only process 'run' and 'setup' keys
        if key in data and isinstance(data[key], str):
            output[key] = data[key].strip().split("\n")  # Convert string to list of lines
        else:
            output[key] = data[key]

    return output 



def prettify_task_config(task_config:Dict[str, Any]):
  return convert_multiline_to_list(task_config)

if __name__ == "__main__":
    load_dotenv(str(Path(__file__).parents[5]/".env"))
    task_config = yaml.safe_load(open(Path(f"{__file__}").parents[1] / "test/configs/simple_sky.yaml"))
    # zenml_orchestration_run_skypilot_task(task_config=task_config["steps"]["test_sky_simple"]["parameters"]["sky_config"],
    #                                       zenml_store_url=os.getenv("ZENML_HOST"),
    #                                       zenml_store_api_key=os.getenv("ZENML_SKY_SERVICE_ACCOUNT_KEY"))

    # run_skypilot_task(task_config=task_config["steps"]["test_sky_simple"]["parameters"]["sky_config"])
