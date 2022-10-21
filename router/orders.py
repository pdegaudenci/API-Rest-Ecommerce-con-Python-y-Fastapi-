## Sistema de enrutado para los pedidos
from fastapi import APIRouter

# Modulo APIRouter permite crear sistemas de rutas
orders_router = APIRouter()

@orders_router.get('/orders')
def get_orders():
    return "Hola mundo"