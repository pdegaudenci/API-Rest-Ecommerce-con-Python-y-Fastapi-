from typing import Optional, Union, List
from pydantic import BaseModel


class Status_Option(BaseModel):
    status_type: str

class Product_categories(BaseModel):
    name : str
    description: str

class Memory_option(BaseModel):
    memory_capacity: int
    capacity_type : str


class Product(BaseModel):
    name : str
    price: float
    description:str
    track_iventory: bool
    qty : int
    width:float
    weight: float
    length: float
    height: float
    image_url : str 
    seo_title :str
    seo_desc :str
    color: str
    Status: Status_Option
    Category: Product_categories
    Memory: Memory_option