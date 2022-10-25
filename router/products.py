## Sistema de enrutado para los pedidos
from fastapi import APIRouter
from models.models import Product, Status
from schemas.schemas_validation import Product_create, Product_update
from config.db_config import session

# Modulo APIRouter permite crear sistemas de rutas
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


@products_router.post('/product')
def create_product(product:Product_create):
    # TODO Verificar si los id de categoria, status y memory existen en sus respectivas tablas (HttpException)
    # Obtengo ultimo registro insertado en la tabla --> obtengo sku de ese producto y le sumo 1 unidad, lo que nos resultara en el nuevo sku 
    # del producto a crear
    obj = session.query(Product).order_by(Product.sku.desc()).first()
    producto = Product(obj.sku +1,product.name,product.price,product.description,product.track_iventory,product.qty,product.weight,product.height,product.width,product.length,
                        product.image_url,product.seo_title,product.seo_desc,product.color,product.status,product.category,product.memory)
    # Agrego producto
    session.add(producto)
    #Ejecuto transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos)
    session.commit()
    session.refresh(producto)
    return product

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
    session.query(Product).filter(Product.sku == sku).update(values, synchronize_session='fetch')
    session.commit()
    return product