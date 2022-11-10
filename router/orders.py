## Sistema de enrutado para los pedidos
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.order_validation import Order_create,Customer
from config.db_config import session
from services import orders_service
from models.models import products_orders
# Modulo APIRouter permite crear sistemas de rutas
orders_router = APIRouter()


@orders_router.get(path='/orders',status_code=status.HTTP_200_OK ,summary="Get all orders", tags=["Orders"])
def get_orders(): 
    return orders_service.get_orders()

@orders_router.get(path='/order/{id}',status_code=status.HTTP_200_OK ,summary="Get order by id", tags=["Orders"])
def get_order(id:int): 
    result = orders_service.get_order_byid(id)
    return result

@orders_router.get('/customers')
def get_customers():
    result = session.query(Customer)
    return result
    
@orders_router.post(path='/order',status_code=status.HTTP_201_CREATED ,summary="Create order", tags=["Orders"])
def create_order(order: Order_create):
    result,product_ok = orders_service.create_order(order)
    print(result)
    if product_ok["status"]==False:
        raise HTTPException(404,detail=product_ok["msg"])
    print(result)
    return  JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_201_CREATED) 
