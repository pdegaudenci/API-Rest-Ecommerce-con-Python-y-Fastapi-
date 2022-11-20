import os
from os.path import join, dirname
# Dotenv es un módulo de dependencia cero que carga las variables en las variables de entorno del archivo.env en process.env.
#El dotenv se utiliza para leer el par de clave y valor del archivo .env y agregarlo a la variable de entorno. Podemos usarlo para administrar la configuración de la aplicación
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
# Cargo el archivo con variables de entorno 
load_dotenv(dotenv_path=dotenv_path)


"""
    Clase que contiene constantes con valores de configuracion que son usados por la API durante su ciclo de ejecución-
"""
class Settings:

    PROJECT_NAME:str = "E-commerce API"
    PROJECT_VERSION: str = "1.0.0"
    # Obtener / leer valores de variables de entorno
    POSTGRES_USER : str = os.environ.get("USER","USERNAME")
    POSTGRES_PASSWORD = os.environ.get("PASSWORD")
    POSTGRES_SERVER : str = os.environ.get("HOST","localhost")
    POSTGRES_PORT : str = os.environ.get("PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.environ.get("DATABASE","test")
    # Construccion de URL de Conexion de la BBDD -->  'motorBDD+driver://usuario:password@IPServidor:puerto/nombreBBDD'
    DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # Valores para generacion de token (secret key y tiempo de validez)
    secret_key: str = os.getenv('SECRET_KEY')
    token_expire: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

    # Datos usuarios admin
    admin_user = os.getenv('ADMIN')
    pwd_admin =os.getenv('PASSWORD_ADMIN')
# Instanciacion de la clase para usar los atributos del objetos en los otros modulos que asi lo requieran
settings = Settings()