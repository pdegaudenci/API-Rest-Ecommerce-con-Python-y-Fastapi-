## Sistema de enrutado para los pedidos
from fastapi import APIRouter
from models.models import Order,Customer
from config.db_config import session

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
    


@orders_router.post('/orders')
def create_order():
    result = session.query(Customer).get()
    return result
