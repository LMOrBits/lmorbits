from pathlib import Path

from dotenv import load_dotenv
from loguru import logger


if __name__ == "__main__":
    main_dir = Path(__file__).parents[4]
    secrets_path = main_dir / "secrets/ml/secrets"
    logger.info(f"Loading secrets from {secrets_path}")
    load_dotenv(secrets_path / ".env")
