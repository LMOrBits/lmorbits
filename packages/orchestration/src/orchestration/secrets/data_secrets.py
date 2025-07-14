import argparse
from pathlib import Path

from data.utils.lakefs import LakeFSCredentials
from dotenv import load_dotenv
from loguru import logger
from zenml.client import Client


def get_lakefs_credentials() -> LakeFSCredentials:
    secret = Client().get_secret("lakefs_credentials")
    credentials = LakeFSCredentials(
        endpoint_url=secret.secret_values["LAKECTL_SERVER_ENDPOINT_URL"],
        access_key_id=secret.secret_values["LAKECTL_CREDENTIALS_ACCESS_KEY_ID"],
        secret_access_key=secret.secret_values["LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY"],
        namespace=secret.secret_values["LAKECTL_NAMESPACE"],
    )
    return credentials


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage LakeFS credentials.")
    parser.add_argument("--create", action="store_true", help="Create LakeFS credentials.")
    parser.add_argument("--delete", action="store_true", help="Delete LakeFS credentials.")
    parser.add_argument("--get", action="store_true", help="Get LakeFS credentials.")
    args = parser.parse_args()

    main_dir = Path(__file__).parents[3]
    lmorbits_dir = main_dir.parents[1]
    load_dotenv(lmorbits_dir / ".env")
    load_dotenv(main_dir / ".env", override=True)
    logger.info("Loading credentials from .env file from \n"
                f"{main_dir}/.env \n"
                f"{lmorbits_dir / '.env'}")

    credentials = LakeFSCredentials.from_env()
    client = Client()
    if args.get:
        logger.info(f"LakeFS credentials: {credentials}")

    if args.create:
        client.create_secret(
            name="lakefs_credentials",
            values={
                "LAKECTL_SERVER_ENDPOINT_URL": credentials.endpoint_url,
                "LAKECTL_CREDENTIALS_ACCESS_KEY_ID": credentials.access_key_id,
                "LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY": credentials.secret_access_key,
                "LAKECTL_NAMESPACE": credentials.namespace,
            },
        )
        logger.info(
            "Credentials created for lakefs_credentials. You can now get the credentials by running `get_lakefs_credentials()`"
        )
    elif args.delete:
        if client.get_secret("lakefs_credentials"):
            client.delete_secret("lakefs_credentials")
            logger.info("Credentials for lakefs_credentials have been deleted.")
