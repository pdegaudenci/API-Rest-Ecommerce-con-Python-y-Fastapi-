## Sistema de enrutado para los pedidos
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.order_validation import Order_create,Customer
from config.db_config import session
from services import orders_service
# Modulo APIRouter permite crear sistemas de rutas
orders_router = APIRouter()


@orders_router.get('/orders')
def get_orders(): 
    pass


@orders_router.get('/customers')
def get_customers():
    result = session.query(Customer)
    return result
    


@orders_router.post('/order')
def create_order(order: Order_create):
    result = orders_service.create_order(order)
    print(result["customer"])
    return  JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK) 
