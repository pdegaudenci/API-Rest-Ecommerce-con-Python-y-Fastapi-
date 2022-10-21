from importlib.metadata import metadata
from sqlalchemy import create_engine,MetaData
from .config import settings


CONECTION_URL = settings.DATABASE_URL

engine = create_engine(CONECTION_URL)

meta = MetaData()

connector = engine.connect()

