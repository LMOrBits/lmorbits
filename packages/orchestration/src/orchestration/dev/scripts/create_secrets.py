from zenml.client import Client
from dotenv import load_dotenv
from pathlib import Path
from data.utils.lakefs import LakeFSCredentials

load_dotenv(Path(__file__).parent / ".env")

credentials = LakeFSCredentials.from_env()

client = Client()
client.create_secret(
    name="lakefs_credentials",
    values={
        "LAKECTL_SERVER_ENDPOINT_URL": credentials.endpoint_url,
        "LAKECTL_CREDENTIALS_ACCESS_KEY_ID": credentials.access_key_id,
        "LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY": credentials.secret_access_key,
        "LAKECTL_NAMESPACE": credentials.namespace
    }
)