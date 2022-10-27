from config.db_config import session
from models.models import Product, Status, Memory,Categories


def validate_product_FKs(product, operation):
    result = None
    #Verificar si los id de categoria, status y memory existen en sus respectivas tablas 
    busqueda = validate_fk(Categories,Categories.category_id,product.category)!=None and validate_fk(Status,Status.id_status,product.status) != None and  validate_fk(Memory,Memory.id_memory, product.memory) != None
    if busqueda:
        # Obtengo ultimo registro insertado en la tabla --> obtengo sku de ese producto y le sumo 1 unidad, lo que nos resultara en el nuevo sku 
        # del producto a crear
        obj = session.query(Product).order_by(Product.sku.desc()).first()
        producto = Product(obj.sku +1,product.name,product.price,product.description,product.track_iventory,product.qty,product.weight,product.height,product.width,product.length,
                        product.image_url,product.seo_title,product.seo_desc,product.color,product.status,product.category,product.memory)
        result = producto
    
    return result

def validate_fk(fk,fk_request, table):
    return session.query(table).filter(fk == fk_request).first()

    