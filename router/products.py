## Sistema de enrutado para los pedidos

from fastapi import APIRouter,HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from services import products_service
from models.models import Product, Status, Memory,Categories
from schemas.schemas_validation import Product_create, Product_update
from config.db_config import session

# Modulo APIRouter permite crear sistemas de  para ejecutar peticiones para realizar operaciones sobre products
products_router = APIRouter()


@products_router.get('/products')
def get_products():
    result = session.query(Product).all()
    if len(result) == 0:
        return "no hay datos"
    return result

@products_router.get('/product/{sku}')
def get_product(sku : int):
    result = session.query(Product).filter(Product.sku == sku).first()
    if result :
        return result
    return "No hay datos"

@products_router.get('/products/')
def get_products_with_limit(skip:int ,limit: int):
    result = session.query(Product).offset(skip).limit(limit).all()
    if result:
        return result
    return "No hay datos"

@products_router.delete('/product/{sku}')
def delete_product(sku : int ):
    result = session.query(Product).filter(Product.sku == sku).delete()
    return result

## CREACION DE PRODUCTOS
@products_router.post(path="/product",
    status_code=status.HTTP_201_CREATED ,
    summary="Create a new product",
    tags=["Products"])
def create_product(product:Product_create):
    respuesta = None
    producto = products_service.validate_product_FKs(product)
    if producto != None:
        # Ejecuto transaccion para agregar el producto
        try:
            # Agregar producto
            session.add(producto)
            #Ejecutar transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos)
            session.commit()
            session.refresh(producto)
            respuesta = JSONResponse(content={"status_code":status.HTTP_201_CREATED, "data":jsonable_encoder(product)})
        except: 
            # En caso que no se pueda ejecutar la insercion, hago rollback de la trasaccion y lanzo un HttpException
            session.rollback()
            raise HTTPException(404, detail='Transaction Error product')    
    else:
        raise HTTPException(404, detail='category or status or memory not found by id')    
    return respuesta


@products_router.put('/product')
def update_product(sku:int, product: Product_update):
    
    # Conversiond e body en diccionario para poder recorrerlo 
    values = product.dict()
    # Recorro el diccionario para eliminar valores None (Obtengo claves de una copia del diccionario porque durante cada iteracion el diccionario original cambia de tamaño)
    for key in values.copy():
        if values[key] == None :
            #Si valor es nulo elimino clave del diccionario --> Valor None significa que ese campo no sea ha enviado para actualizar
            values.pop(key)
    #  Actualizo valores de campos del registro con una query
    if "category" or "status" or "memory" in values:
            products_service.validate_fk(Categories.id_category,product.category,Categories)
            products_service.validate_fk(Status.id_status,product.status,Status)
            products_service.validate_fk(Memory.id_memory,product.memory,Memory)
        
    session.query(Product).filter(Product.sku == sku).update(values, synchronize_session='fetch')
    session.commit()
    return product