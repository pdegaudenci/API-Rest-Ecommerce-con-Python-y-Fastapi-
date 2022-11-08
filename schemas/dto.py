
from fastapi.encoders import jsonable_encoder


def DTO_product(product):
    product_json = jsonable_encoder(product)
    product_json["Status"].pop("id_status")
    product_json["Memory"].pop("id_memory")
    product_json["Categories"].pop("id_category")
    keys_delete = ["status_id","category_id","memory_id"]
    [product_json["Product"].pop(key) for key in keys_delete] 
    return product_json

def order_dto(order):
  return order
