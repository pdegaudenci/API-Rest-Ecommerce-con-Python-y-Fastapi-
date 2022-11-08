from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import date
from datetime import datetime
from config.db_config import session,engine
from models.models import Order,Customer,products_orders
from services.products_service import get_product
from models.models import Product
from schemas.dto import order_dto
#Variable global que contabiliza numero de order
NUMBER_ORDER = 3

def inc_number():
  global NUMBER_ORDER 
  NUMBER_ORDER +=1

def create_order(order):
    product_ok = verify_product_bysku(order.products)
    result= {"order": None, "products":None, "customer":None}

    if product_ok["status"]==True:
        date =datetime.now()
        ammount_total,products_detail = calculate_total(order.products)
        customer = create_customer(order.customer)
        last_order = session.query(Order).order_by(Order.id_order.desc()).first()
        if last_order == None:
          # Uso de variable global (No declarada en esta funcion)
          global NUMBER_ORDER
          new_id = NUMBER_ORDER
        else:
          new_id = last_order.id_order + 1
        new_order = Order(new_id,customer,ammount_total,order.shipping_address,order.order_address,order.order_email,date,"NEW")
        # Agregar order
        session.add(new_order)
        #Ejecutar transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos) --> Actualizao BBDDD
        session.commit()
        inc_number()
        # Mi respuesta va a contener : pedido, detalles de productos pedidos y datos del cliente
        result["order"]=new_order
        result["products"]=products_detail
        result["customer"]=get_customer(customer.id_customer)
        session.refresh(new_order)
        session.close()
    else :
        return product_ok.msg
    return result

def create_order2(order):
    product_ok = verify_product_bysku(order.products)
    result= {"order": None, "products":None, "customer":None}
    try:
      if product_ok["status"]==True:
        date =datetime.now()
        ammount_total,products_detail = calculate_total(order.products)
        customer = create_customer(order.customer)
        last_order = session.query(Order).order_by(Order.id_order.desc()).first()
        if last_order == None:
          # Uso de variable global (No declarada en esta funcion)
          global NUMBER_ORDER
          new_id = NUMBER_ORDER
        else:
          new_id = last_order.id_order + 1
        new_order = Order(new_id,customer,ammount_total,order.shipping_address,order.order_address,order.order_email,date,"NEW")
        # Agregar order
        session.add(new_order)
        #Ejecutar transaccion (Podria ejecutar previamente varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos) --> Actualizao BBDDD
        session.commit()
        inc_number()
        session.refresh(new_order)
        session.close()
        # Mi respuesta va a contener : pedido, detalles de productos pedidos y datos del cliente
        result["order"]=new_order
        result["products"]=products_detail
        result["customer"]=get_customer(customer.id_customer)
      else :
        return product_ok.msg
    except:
          # En caso que no se pueda ejecutar la insercion, hago rollback de la trasaccion y lanzo un HttpException
          # TODO Borrar cliente 
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
        total = product.quantity * producto.price
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
    if verify_customer(customer.email) == True :
      respuesta = session.query(Customer).filter(Customer.email == customer.email).first()
    else:
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
    if session.query(Customer).filter(Customer.email == email).first() != None:
      customer_exist = True
    return customer_exist
  
def update_stock(sku):
  pass

def get_customer(id):
  print(id)
  result = session.query(Customer).filter(Customer.id_customer == id).first()
  print(result)
  return result

