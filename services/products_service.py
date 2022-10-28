from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status

from config.db_config import Session, session
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

def get_product(sku):
    return session.query(Product).filter(Product.sku == sku).first()

def delete_product(sku):
    try:
        session.query(Product).filter(Product.sku == sku).delete()
        session.commit()
        session.close()
    except:
        session.rollback()
        session.close()
        raise HTTPException(404, detail='Delete Transaction Error')
    return f"Product with sku : {sku} deleted succesfully"

def create_product(product):
     # Obtengo ultimo registro insertado en la tabla --> obtengo sku de ese producto y le sumo 1 unidad, lo que nos resultara en el nuevo sku 
     # del producto a crear
    respuesta = None
    obj = session.query(Product).order_by(Product.sku.desc()).first()
    producto = Product(obj.sku +1,product.name,product.price,product.description,product.track_iventory,product.qty,product.weight,product.height,product.width,product.length,
                        product.image_url,product.seo_title,product.seo_desc,product.color,product.status,product.category,product.memory)
     # Ejecuto transaccion para agregar el producto
    try:
        # Agregar producto
        session.add(producto)
        #Ejecutar transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos)
        session.commit()
        session.refresh(producto)
        session.close()
        respuesta = JSONResponse(status_code=status.HTTP_201_CREATED,content=jsonable_encoder(product))
    except: 
            # En caso que no se pueda ejecutar la insercion, hago rollback de la trasaccion y lanzo un HttpException
            session.rollback()
            session.close()
            raise HTTPException(404, detail='Transaction Error product')
    return respuesta

def update_product(product,sku,values):
    try:
        session.query(Product).filter(Product.sku == sku).update(values)
        print("sku: ")
        print(sku)
        print("values:")
        session.commit()
        respuesta = JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(session.query(Product).filter(Product.sku == sku).first()))
        session.close()
    except: 
            session.rollback()
            session.close()
            raise HTTPException(404, detail='Product Transaction Error / Id not found ')
    return respuesta

    