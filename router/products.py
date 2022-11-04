## Sistema de enrutado para los pedidos

from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from services import products_service
from schemas import dto
from models.models import Product
from schemas.product_validation import Product_create, Product_update
from config.db_config import session

# Modulo APIRouter permite crear sistemas de  para ejecutar peticiones para realizar operaciones sobre products
products_router = APIRouter()

# OBTENCION DE PRODUCTOS : LISTA TOTAL, POR SKU Y RANGO DE PRODUCTOS
@products_router.get(path='/products',status_code=status.HTTP_200_OK ,summary="Get all products", response_model=List)
def get_products():
    result = products_service.get_products()
    if len(result) == 0 :
        raise HTTPException(404, detail='No products availables')  
    return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(result))

@products_router.get(path='/product/{sku}',status_code=status.HTTP_200_OK ,summary="Get product by SKU", tags=["Products"])
def get_product(sku : int ):
    result = products_service.get_product(sku)
    if result == None :
        raise HTTPException(404, detail=f'Product not found by sku {sku}')
    response = dto.DTO_product(result)
    return JSONResponse(status_code=status.HTTP_200_OK,content=response)

@products_router.get(path='/products_page/',status_code=status.HTTP_200_OK ,summary="Get products in range", tags=["Products"])
def get_products_with_limit(skip:int ,limit: int):
    return products_service.get_products_by_page(skip,limit)
    

## BORRADO DE PRODUCTO POR SU ID O SKU
@products_router.delete(path='/product/{sku}',status_code=status.HTTP_202_ACCEPTED ,summary="Delete one product by SKU", tags=["Products"])
def delete_product(sku : int ):
    result = products_service.get_product(sku)
    if result == None:
        raise HTTPException(404, detail=f'Product not found by sku {sku}') 
    else :
        response = products_service.delete_product(sku)
    return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_202_ACCEPTED)
    
## CREACION DE PRODUCTOS
@products_router.post(path="/product",status_code=status.HTTP_201_CREATED ,summary="Create a new product", tags=["Products"])
def create_product(product:Product_create = Depends()):
    # Verificacion de id de categoria,status o memoria sean FKs validos
    result = products_service.validate_product_FKs(product,"create")
    if result:
         respuesta=products_service.create_product(product)  
    else:
        raise HTTPException(404, detail='category or status or memory not found by id')    
    return JSONResponse(content=jsonable_encoder(respuesta), status_code=status.HTTP_201_CREATED)

# ACTUALIZACION DE PRODUCTO
@products_router.put(path='/product',status_code=status.HTTP_200_OK ,summary="Update product's values by SKU", tags=["Products"])
def update_product(sku:int, product: Product_update= Depends()):
    # Conversiond e body en diccionario para poder recorrerlo 
    values = product.dict()
    # Recorro el diccionario para eliminar valores None (Obtengo claves de una copia del diccionario porque durante cada iteracion el diccionario original cambia de tamaño)
    for key in values.copy():
        if values[key] == None :
            #Si valor es nulo elimino clave del diccionario --> Valor None significa que ese campo no sea ha enviado para actualizar
            values.pop(key)
    #  Verificar si las FKs son validas
    result = products_service.validate_product_FKs(product,"update")
    if result:
        # Actualizar campos de producto
        respuesta = products_service.update_product(sku,values)
    else:
        raise HTTPException(404, detail='category or status or memory id error')    
    return JSONResponse(content=jsonable_encoder(respuesta), status_code=status.HTTP_200_OK) 