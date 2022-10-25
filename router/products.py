## Sistema de enrutado para los pedidos
from fastapi import APIRouter
from models.models import Product, Status
from schemas.schemas_validation import Product_create
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
    status = session.query(Product).filter(Status.status_type == product.status.status_type).first()
    if status :
        id = status.id_status
        producto = Product(product.name,product.price,product.description,product.track_iventory,product.qty,product.weight,product.height,product.width,product.length,
                        product.image_url,product.seo_title,product.seo_desc,product.color,id,product.category_id,product.memory_id)
    product.add()
    product.commit()
    result = session.query(Product)
    return result
    


@products_router.put('/product')
def update_product():
    result = session.query(Product).get()
    return result