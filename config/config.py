import os
#for loading environment variables
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME:str = "E-commerce API"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.getenv("USERNAME")
    POSTGRES_PASSWORD = os.getenv("PASSWORD")
    POSTGRES_SERVER : str = os.getenv("HOST","localhost")
    POSTGRES_PORT : str = os.getenv("PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("DATABASE","test")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()