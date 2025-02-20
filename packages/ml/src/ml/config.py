import os
from configparser import ConfigParser
from pathlib import Path

from dotenv import load_dotenv
from omegaconf import OmegaConf


def enable_multipart_upload():
    os.environ["MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD"] = "true"
    # For example, use a 50 MB threshold: if file size >= 50 MB, use multipart upload.
    os.environ["MLFLOW_MULTIPART_UPLOAD_MINIMUM_FILE_SIZE"] = str(50 * 1024 * 1024)
    # Set chunk size to 10 MB (adjust based on your network/storage performance).
    os.environ["MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE"] = str(10 * 1024 * 1024)

def config():
    config_path = Path(__file__).parents[2] / "configs" / "finetuning.yaml"
    model_config = OmegaConf.load(config_path)
    OmegaConf.resolve(model_config)

    # Todo remove this from here
    data_env_path = Path(__file__).parents[2] / "secrets/.env"
    load_dotenv(data_env_path)
    mlflow_config = ConfigParser()
    mlflow_config_path = Path(__file__).parents[2] / "secrets/my_auth_config.ini"
    mlflow_config.read(mlflow_config_path)
    os.environ["MLFLOW_TRACKING_USERNAME"] = mlflow_config["mlflow"][
        "TRACKING_USERNAME"
    ]
    os.environ["MLFLOW_TRACKING_PASSWORD"] = mlflow_config["mlflow"][
        "TRACKING_PASSWORD"
    ]
    return model_config, mlflow_config
