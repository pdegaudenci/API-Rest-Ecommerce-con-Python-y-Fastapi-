from typing import Optional, Union, List
from pydantic import BaseModel


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
    order_date: str
    order_status : str
    customer : Customer

class Status_Option(BaseModel):
    status_type: str

class Product_categories(BaseModel):
    name : str
    description: str

class Memory_option(BaseModel):
    memory_capacity: int
    capacity_type : str

class Product_create(BaseModel):
    name : str
    price: float
    description:str
    track_iventory: bool
    qty : int
    weight: float
    length: float
    height: float
    image_url : str 
    seo_title :str
    seo_desc :str
    color: str
    status: int
    category: int
    memory: int



