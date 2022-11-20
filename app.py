from fastapi import FastAPI
from router.orders import orders_router
from router.products import products_router 
from router.user import user_router
from config.db_config import session
from models.models import User
from schemas.auth_schema import User_Admin
from config.config import settings
from services.user_service import create_user_admin



app = FastAPI(
    title= "Ecommerce API Rest",
    description= "",
    openapi_tags=[{
    "name": "Ecommerce API Rest",
    "description":""
    }])

#Creacion de un usuario admin por defecto (valores de usuario y password en archivo config/.env)
if session.query(User).filter(User.level == "admin").first() == None:
    user_admin = User_Admin(email=settings.admin_user,password=settings.pwd_admin)
    create_user_admin(user=user_admin)

# uvicorn archivo:nombreInstancia (uvicorn app:app)

# CREO SISTEMA DE ENRUTADO DE MI API

# Agrego a la aplicacion enrutamiento para mis pedidos 
app.include_router(orders_router)

# Enrutamiento para productos
app.include_router(products_router)

# Enrutamiento para usuarios
app.include_router(user_router)
