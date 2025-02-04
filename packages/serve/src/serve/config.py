import os
import mlflow
from pathlib import Path
from configparser import ConfigParser

def config_init():
    config_mlflow = ConfigParser()
    dir_path = Path(__file__).parent / 'secrets' / 'my_auth_config.ini'
    config_mlflow.read(dir_path)
    os.environ['MLFLOW_TRACKING_USERNAME'] = config_mlflow['mlflow']['TRACKING_USERNAME']
    os.environ['MLFLOW_TRACKING_PASSWORD'] = config_mlflow['mlflow']['TRACKING_PASSWORD']
    return config_mlflow

