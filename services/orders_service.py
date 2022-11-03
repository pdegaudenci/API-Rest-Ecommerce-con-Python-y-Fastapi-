from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import session,engine
from models.models import Order,Customer,products_orders
from services.products_service import get_product
from datetime import date
from datetime import datetime

def create_order(order):
    product_ok = verify_product(order.products)
    if product_ok:
        date =datetime.now()
        ammount_total = calculate_total(order.products)
        id_customer = create_customer(order.customer)
        

def verify_product(products):
    pass

def calculate_total(products):
    pass

def create_customer(order.customer):
    pass

def verify_customer(email):
    pass

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
