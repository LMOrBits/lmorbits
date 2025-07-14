import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel
from zenml.client import Client


class MLFSCredentials(BaseModel):
    tracking_uri: str
    tracking_username: str
    tracking_password: str

def get_ml_credentials() -> MLFSCredentials:
    secret = Client().get_secret("ml_credentials")
    return MLFSCredentials(
        tracking_uri=secret.secret_values["MLFLOW_TRACKING_URI"],
        tracking_username=secret.secret_values["MLFLOW_TRACKING_USERNAME"],
        tracking_password=secret.secret_values["MLFLOW_TRACKING_PASSWORD"],
    )


if __name__ == "__main__":
    main_dir = Path(__file__).parents[4]
    logger.info(f"Loading secrets from {main_dir}")
    load_dotenv(main_dir / ".env")

    parser = argparse.ArgumentParser(description="Manage LakeFS credentials.")
    parser.add_argument("--create", action="store_true", help="Create LakeFS credentials.")
    parser.add_argument("--delete", action="store_true", help="Delete LakeFS credentials.")
    args = parser.parse_args()


    client = Client()
    if args.create:
        ml_credentials = MLFSCredentials(
            tracking_uri=os.getenv("MLFLOW_TRACKING_URI", ""),
            tracking_username=os.getenv("MLFLOW_TRACKING_USERNAME", ""),
            tracking_password=os.getenv("MLFLOW_TRACKING_PASSWORD", ""),
        )
        client.create_secret(
            name="ml_credentials",
            values={
                "MLFLOW_TRACKING_URI": ml_credentials.tracking_uri,
                "MLFLOW_TRACKING_USERNAME": ml_credentials.tracking_username,
                "MLFLOW_TRACKING_PASSWORD": ml_credentials.tracking_password,
            },
        )
        logger.info(
            "Credentials created for ml_credentials. You can now get the credentials by running `get_ml_credentials()`"
        )
    elif args.delete:
        if client.get_secret("ml_credentials"):
            client.delete_secret("ml_credentials")
            logger.info("Credentials for ml_credentials have been deleted.")
