
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import session,engine
from models.models import Product, Status, Memory,Categories


def validate_product_FKs(product,operation):
    result = True
    #Verificar si los id de categoria, status y memory existen en sus respectivas tablas
    if operation == "create":
        result = validate_fk(Categories,Categories.id_category,product.category)!=None and validate_fk(Status,Status.id_status,product.status) != None and  validate_fk(Memory,Memory.id_memory, product.memory) != None
    else:
        if product.category !=None:
            result = validate_fk(Categories,Categories.id_category,product.category) != None
        if product.status != None:
            result = validate_fk(Status,Status.id_status,product.status) != None 
        if product.memory != None:
            result = validate_fk(Memory,Memory.id_memory, product.memory)!= None
    return result

def validate_fk(table,fk,fk_request):
    return session.query(table).filter(fk == fk_request).first()

# Retorna producto por sku, uniendo los respectivos atributos con las tablas relacionadas
def get_product(sku):
    try:
        response = session.query(Product, Status, Memory, Categories).join(Product.status_product, Product.memory_product, Product.category_product).filter(Product.sku == sku).first()
        session.close()
    except:
        session.rollback()
        session.close()
        raise HTTPException(404, detail='Transaction Error') 
    return response

def get_products():
    # Habilita el verbose en consola de consulta SQL hecha por ORM
    #engine.echo = True
    try:
        response =session.query(Product, Status, Memory, Categories).join(Product.status_product, Product.memory_product, Product.category_product).all()
        session.close()
    except:
        session.rollback()
        session.close()
        raise HTTPException(404, detail='Transaction Error') 
    return response

def get_products_by_page(skip:int ,limit: int):
    result = session.query(Product).offset(skip).limit(limit).all()
    if result:
        return result
    return HTTPException(404, detail=f'No products in range {skip} - {skip+limit}',headers={"data":"no data"}) 

def delete_product(sku):
    try:
        session.query(Product).filter(Product.sku == sku).delete()
        session.commit()
    except:
        session.rollback()
        session.close()
        raise HTTPException(404, detail='Delete Transaction Error')
    response = f'Product {sku} was deleted succesfully'
    return response

def create_product(product):
     # Obtengo ultimo registro insertado en la tabla --> obtengo sku de ese producto y le sumo 1 unidad, lo que nos resultara en el nuevo sku 
     # del producto a crear
    respuesta = None
    obj = session.query(Product).order_by(Product.sku.desc()).first()
    new_sku =obj.sku +1
    producto = Product(obj.sku +1,product.name,product.price,product.description,product.track_iventory,product.qty,product.weight,product.height,product.width,product.length,
                        product.image_url,product.seo_title,product.seo_desc,product.color,product.status,product.category,product.memory)
     # Ejecuto transaccion para agregar el producto
    try:
        # Agregar producto
        session.add(producto)
        #Ejecutar transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos)
        session.commit()
        session.refresh(producto)
        respuesta = get_product(new_sku)
        session.close()
    except: 
            # En caso que no se pueda ejecutar la insercion, hago rollback de la trasaccion y lanzo un HttpException
            session.rollback()
            session.close()
            raise HTTPException(404, detail='Transaction Error product')
    # Recupera de la BBDD el producto creado y lo retorna como respuesta
    return respuesta

def update_product(sku,values):
    try:
        session.query(Product).filter(Product.sku == sku).update(values)
        session.commit()
        session.close()
    except: 
            session.rollback()
            session.close()
            raise HTTPException(404, detail='Product Transaction Error / Id not found ')
     # Recupera de la BBDD el producto actualizado y lo retorna como respuesta
    return get_product(sku)

    