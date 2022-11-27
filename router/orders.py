## Sistema de enrutado para los pedidos
from fastapi import APIRouter, status, HTTPException,Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.order_validation import Order_create,Order_update
from middleware.mw import get_current_user
from config.db_config import session
from services import orders_service,user_service
from schemas.dto import order_dto
from models.models import Customer
from schemas.auth_schema import User
# Modulo APIRouter permite crear sistemas de rutas para los pedidos
orders_router = APIRouter()

"""
    SE DEFINEN METODOS DE OPERACION SOBRE PEDIDOS --> Todas los endpoints están protegidos (Los usuarios deben estar autenticados)
"""
""" Obtener todos los pedidos --> Solamente user admin puede realizar esta operacion"""
@orders_router.get(path='/orders',summary="Get all orders", tags=["Orders"],)
def get_orders(user: User = Depends(get_current_user)):
    #Si username es administrador , se obtienen todas las orders
    if user.level =="admin":
        result = orders_service.get_orders()
    else:
        #En este caso se obtienen solamente las orders del usuario
        result = orders_service.getOrder_byuser(user.email)
    result = jsonable_encoder(result)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK) 

""" Obtener pedido por id -->  user admin y usuario que creo la orden pueden realizar esta operacion"""
@orders_router.get(path='/order/{id}',status_code=status.HTTP_200_OK ,summary="Get order by id", tags=["Orders"])
def get_order(id:int,user: User = Depends(get_current_user)):
    order=orders_service.get_order_byid(id)
    if user.level=="admin" or order["order"].user_id == user.email: 
        result = JSONResponse(content=jsonable_encoder(order), status_code=status.HTTP_200_OK) 
    else:
        result = JSONResponse(content=jsonable_encoder({"response:":"No authorized method"}), status_code=status.HTTP_403_FORBIDDEN) 
    return result 

""" Obtener todos los datos de los clientes --> Solamente user admin puede realizar esta operacion"""
@orders_router.get(path='/customers',status_code=status.HTTP_200_OK ,summary="Get all customer", tags=["Customers && users"])
def get_customers(user: User = Depends(get_current_user)):
    if user.level =="admin":
        result = user_service.get_customers()
        result = JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK) 
    else :
        result = JSONResponse(content=jsonable_encoder({"response:":"No authorized method"}), status_code=status.HTTP_403_FORBIDDEN) 
    return result

""" Crear un pedido (usuario registrado)"""
@orders_router.post(path='/order',status_code=status.HTTP_201_CREATED ,summary="Create order", tags=["Orders"])
def create_order(order: Order_create,user: User = Depends(get_current_user)):
    result,product_ok = orders_service.create_order(order,user)
    if product_ok["status"]==False:
        raise HTTPException(404,detail=product_ok["msg"])
    result = order_dto(result)
    return  JSONResponse(content=result, status_code=status.HTTP_201_CREATED) 

""" Borrar pedido por id --> user admin y usuario que creo la orden pueden realizar esta operacion"""
@orders_router.delete(path='/order/{id}',status_code=status.HTTP_201_CREATED ,summary="delete order by id", tags=["Orders"])
def delete_order(id:int,user: User = Depends(get_current_user)):
    order=orders_service.get_order_byid(id)
    if user.level=="admin" or order["order"].user_id == user.email: 
        result = orders_service.delete_order(id,user)
        if result==False:
            raise HTTPException(404,detail="La orden no pudo ser borrada")
    else:
        return JSONResponse(content={"response":"Forbidden"}, status_code=status.HTTP_403_FORBIDDEN) 
    return  JSONResponse(content={"response":"Order was deleted succesfully","id":id}, status_code=status.HTTP_204_NO_CONTENT) 

"""Cambiar direccion de entrega del pedido --> user admin y usuario que creo la orden pueden realizar esta operacion"""
@orders_router.put(path='/order/{id}' ,summary="update order by id", tags=["Orders"])
def update_order(id:int,order:Order_update,user: User = Depends(get_current_user)):
    if orders_service.exist_order(id)== True:
        order_obtenida=orders_service.get_order_byid(id)
        if user.level=="admin" or order_obtenida["order"].user_id == user.email: 
            result = orders_service.update_order(id,order)
            if result==False:
                raise HTTPException(404,detail="La orden no pudo ser borrada")
        else:
            return JSONResponse(content={"response":"Forbidden"}, status_code=status.HTTP_403_FORBIDDEN)
    else:
        return JSONResponse(content={"response":"Orden no encontrada"}, status_code=status.HTTP_404_NOT_FOUND) 
    return  JSONResponse(content=jsonable_encoder(order_obtenida), status_code=status.HTTP_200_OK) 


