## Sistema de enrutado para los pedidos
from fastapi import APIRouter
from models.order_model import orders,customers
from config.db_config import connector
# Modulo APIRouter permite crear sistemas de rutas
orders_router = APIRouter()

@orders_router.get('/orders')
def get_orders():
    return connector.execute(orders.select()).fetchall()

