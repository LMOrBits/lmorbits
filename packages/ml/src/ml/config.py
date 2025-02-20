from pathlib import Path
from omegaconf import OmegaConf
from configparser import ConfigParser
import os
from dotenv import load_dotenv


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
