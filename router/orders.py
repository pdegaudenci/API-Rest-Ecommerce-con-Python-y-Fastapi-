## Sistema de enrutado para los pedidos
from fastapi import APIRouter, status, HTTPException,Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.order_validation import Order_create
from middleware.mw import get_current_user
from config.db_config import session
from services import orders_service,user_service
from schemas.dto import order_dto
from models.models import Customer
from schemas.auth_schema import User
# Modulo APIRouter permite crear sistemas de rutas para los pedidos
orders_router = APIRouter()

"""_summary_ : Obtiene todas los pedidos o pedidos de usuario (segun nivel de usuario)

    Raises:
        HTTPException: Error de BBDD al obtener pedidos

    Returns:
        _type_: JSONResponse : lista de pedidos
"""
@orders_router.get(path='/orders',summary="Get all orders", tags=["Orders"],)
def get_orders(user: User = Depends(get_current_user)):
    # Si username es administrador , se obtienen todas las orders
    if user.level =="admin":
        result = orders_service.get_orders()
    else:
        # En este caso se obtienen solamente las orders del usuario
        result = orders_service.getOrder_byuser(user.email)
    result = jsonable_encoder(result)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK) 

@orders_router.get(path='/order/{id}',status_code=status.HTTP_200_OK ,summary="Get order by id", tags=["Orders"])
def get_order(id:int,user: User = Depends(get_current_user)): 
    result = orders_service.get_order_byid(id)
    return result 

@orders_router.get(path='/customers',status_code=status.HTTP_200_OK ,summary="Get all customer", tags=["Customers && users"])
def get_customers(user: User = Depends(get_current_user)):
    result = session.query(Customer).all()
    return result


@orders_router.post(path='/order',status_code=status.HTTP_201_CREATED ,summary="Create order", tags=["Orders"])
def create_order(order: Order_create,user: User = Depends(get_current_user)):

    result,product_ok = orders_service.create_order(order,user)
    if product_ok["status"]==False:
        raise HTTPException(404,detail=product_ok["msg"])
    result = order_dto(result)
    return  JSONResponse(content=result, status_code=status.HTTP_201_CREATED) 

@orders_router.post(path='/order/{id}',status_code=status.HTTP_201_CREATED ,summary="delete order by id", tags=["Orders"])
def delete_order(order: Order_create,user: User = Depends(get_current_user)):
    result,product_ok = orders_service.create_order(order,user)
    print(result)
    if product_ok["status"]==False:
        raise HTTPException(404,detail=product_ok["msg"])
    result = order_dto(result)
    return  JSONResponse(content=result, status_code=status.HTTP_201_CREATED) 

