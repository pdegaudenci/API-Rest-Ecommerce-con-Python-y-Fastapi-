from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import date
from datetime import datetime
from config.db_config import session,engine
from models.models import Order,Customer,products_orders
from services.products_service import get_product
from models.models import Product
from schemas.dto import order_dto



def create_order(order):
    product_ok = verify_product_bysku(order.products)
    result= []
    try:
      if product_ok.status:
        date =datetime.now()
        ammount_total,products_detail = calculate_total(order.products)
        customer = create_customer(order.customer)
        last_order = session.query(Order).order_by(Order.id_order.desc()).first()
        if last_order == None:
          new_id = 1
        else:
          new_id = last_order.id_customer
        new_order = Order(new_id,customer.customer_id,ammount_total,order.shipping_address,order.order_address,order.order_email,date,"NEW")
        # Agregar order
        
        session.add(new_order)
        #Ejecutar transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos) --> Actualizao BBDDD
        session.commit()
        session.refresh(new_order)
        session.close()
        # Mi respuesta va a contener : pedido, detalles de productos pedidos y datos del cliente
        result.append(new_order)
        result.append(products_detail)
        result.append(customer)
      else :
        return product_ok.msg
    except:
          # En caso que no se pueda ejecutar la insercion, hago rollback de la trasaccion y lanzo un HttpException
          session.rollback()
          session.close()
          raise HTTPException(404, detail='Transaction Error order')
    return result
        
# Verificacion de existencia de producto y si hay stock suficiente segun la cantidad pedida
def verify_product_bysku(products):
    result = {"status": True,"msj":""}
    for product in products:
        response = session.query(Product).filter(Product.sku == product.sku).first()
        if response == None:
          result.status =False
          result.msg ="Incorrect sku"
          print("LEGA AQUI")
          break
        if response.qty < product.quantity:
           result.status =False
           result.msg ="quantity unavailable in store`s stock"
           break
    return result

def calculate_total(products):
    total_ammount = 0.0
    products_detail =[]
    product_detail={"product": None, "quantity": 0, "total":0.0}
    for product in products:
        producto = session.query(Product).filter(Product.sku == product.sku).first()
        total = producto.qty * producto.price
        product_detail["product"] = producto
        product_detail["quantity"] = product.quantity
        product_detail["total"] = total
        total_ammount += total
        products_detail.append(product_detail)
    return total_ammount,products_detail

def create_customer(customer):
    respuesta = None
    obj = session.query(Customer).order_by(Customer.id_customer.desc()).first()
    if obj == None:
      new_id = 1
    else:
      new_id =obj.id_customer +1
    new_customer = Customer(new_id,customer.full_name,customer.email,customer.billing_address,customer.default_shipping_address,customer.zip_code,customer.country,customer.phone)
     # Ejecuto transaccion para agregar el cliente
    try:
        # Agregar cliente
        session.add(new_customer)
        #Ejecutar transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos)
        session.commit()
        session.refresh(new_customer)
        respuesta = get_customer(id)
        session.close()
    except: 
            # En caso que no se pueda ejecutar la insercion, hago rollback de la trasaccion y lanzo un HttpException
            session.rollback()
            session.close()
            raise HTTPException(404, detail='Transaction Error customer')
    # Recupera de la BBDD el cliente creado y lo retorna como respuesta
    return respuesta

def verify_customer(email):
    customer_exist = False
    if session.query(Customer).filter(Customer.email == email).first():
      customer_exist = True
    return customer_exist
  
def update_stock(sku):
  pass

def get_customer(id):
  return session.query(Customer).filter(Customer.id_customer == id).first()
"""
"total_ammount": 0,
  "shipping_address": "string",
  "order_address": "string",
  "order_email": "string",
  "order_date": "string",
  "order_status": "string",
  "customer": {
    "full_name": "string",
    "email": "string",
    "billing_address": "string",
    "default_shipping_address": "string",
    "zip_code": "string",
    "country": "string",
    "phone": "string"
  },
  "products": [
    {
      "sku": 0,
      "quantity": 0
    }
  ]
"""