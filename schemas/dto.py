
from fastapi.encoders import jsonable_encoder

# ATRIBUTOS QUE SERAN EXCLUIDOS EN LAS RESPUESTA DE LOS METODOS DEL CONTROLADOR

def DTO_product(product,order):
    product_json = jsonable_encoder(product)
    product_json["Status"].pop("id_status")
    product_json["Memory"].pop("id_memory")
    product_json["Categories"].pop("id_category")
    keys_delete = ["status_id","category_id","memory_id"]
    if order ==True :
      keys_delete.append("qty")
    [product_json["Product"].pop(key) for key in keys_delete] 
    return product_json

def order_dto(order):
  order_json = jsonable_encoder(order)
  products =order_json["products"]
  for product in products:
    product["product"]["Product"].pop("qty")
  order_json["products"]= products
  return order_json
