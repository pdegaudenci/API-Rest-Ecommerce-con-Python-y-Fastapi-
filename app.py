from fastapi import FastAPI, Request,Response
from router.orders import orders_router
from router.products import products_router 
from config.db_config import session
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
#app.include_router(orders_router)

app.include_router(products_router)
