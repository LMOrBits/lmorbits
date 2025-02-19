from dotenv import load_dotenv
from pathlib import Path
from loguru import logger

_env_loaded = False

def load_env(parents_up:int=6):
    global _env_loaded
    
    if _env_loaded:
        return
        
    for i in reversed(range(1,parents_up)):
        path = Path(__file__).parents[i]
        logger.info(f"Loading .env file from {path}/.env")
        if i == parents_up-1:
            load_dotenv(path / ".env")
        else:
            load_dotenv(path / ".env", override=True)
    
    _env_loaded = True


if __name__ == "__main__":
    load_env()
