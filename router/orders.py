## Sistema de enrutado para los pedidos
from fastapi import APIRouter
from schemas.order_validation import Order_create,Customer
from config.db_config import session
from services.orders_service import create_order
# Modulo APIRouter permite crear sistemas de rutas
orders_router = APIRouter()


@orders_router.get('/orders')
def get_orders(): 
    result = session.query(Order).all()
    
    return result

@orders_router.get('/customers')
def get_customers():
    result = session.query(Customer)
    return result
    


@orders_router.post('/order')
def create_order(order: Order_create):
    result = create_order(order)
    return result
