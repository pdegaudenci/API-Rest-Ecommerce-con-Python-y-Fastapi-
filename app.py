from fastapi import FastAPI
from router.orders import orders_router
from router.products import products_router 
from router.user import user_router


app = FastAPI(
    title= "Ecommerce API Rest",
    description= "",
    openapi_tags=[{
    "name": "Ecommerce API Rest",
    "description":""
    }])


# uvicorn archivo:nombreInstancia (uvicorn app:app)

# CREO SISTEMA DE ENRUTADO DE MI API

# Agrego a la aplicacion enrutamiento para mis pedidos 
app.include_router(orders_router)

# Enrutamiento para productos
app.include_router(products_router)

# Enrutamiento para usuarios
app.include_router(user_router)
