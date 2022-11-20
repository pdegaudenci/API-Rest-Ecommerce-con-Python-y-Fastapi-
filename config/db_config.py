from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Leo URL de conexion a BBDD de archivo de configuracion (a traves de objeto de clase Setting definida en archivo config.py)
CONECTION_URL = settings.DATABASE_URL

#El motor se usa principalmente para manejar dos elementos: 
# los pools de conexiones(para manejar las conexiones a la base de datos) 
# y el dialecto a utilizar(configura el dialecto y se encarga de hacer las traducciones necesarias a código SQL propias de cada motor de BBDD)
engine = create_engine(CONECTION_URL)

#Una sesión es  una transacción -->registra una lista de objetos creados, 
#modificados o eliminados dentro de una misma transacción
Session = sessionmaker(bind=engine)
session = Session()

# Base : clase de la que hereden todos los modelos
# y tiene la capacidad de realizar el mapeo correspondiente a partir de la metainformación
Base = declarative_base()

#OTRA OPCION
#meta = MetaData()
#connector = engine.connect()

