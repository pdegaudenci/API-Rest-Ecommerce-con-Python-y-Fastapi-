from fastapi import FastAPI
from router.orders import orders_router

app = FastAPI(
    title= "Ecommerce API Rest",
    description= "",
    openapi_tags=[{
    "name": "Ecommerce API Rest",
    "description":""
    }])

# uvicorn archivo:nombreInstancia (uvicorn main:app)

# CREO SISTEMA DE ENRUTADO DE MI API
# Agrego a la aplicacion enrutamiento para mis pedidos 
app.include_router(orders_router)

