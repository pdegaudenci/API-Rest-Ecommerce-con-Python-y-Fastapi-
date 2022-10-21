from sqlalchemy import create_engine, Meta
from config import settings
# URL conexion: 'motorBDD+driver://usuario:password@IPServidor:puerto/nombreBBDD'
CONECTION_URL = settings.DATABASE_URL
engine = create_engine(CONECTION_URL)

meta = Meta()

connector = engine.connect()

