from typing import Optional, Union, List
from pydantic import BaseModel

class Product_request(BaseModel):
    sku : int
    quantity : int

class Customer(BaseModel):
    full_name : str
    email : str
    billing_address : str
    default_shipping_address: str
    zip_code: str
    country: str
    phone : str

class Order_create(BaseModel):
    total_ammount : float
    shipping_address : str
    order_address: str
    order_email: str
    order_status : str
    customer : Customer
    products: List[Product_request]
    payment_method: str