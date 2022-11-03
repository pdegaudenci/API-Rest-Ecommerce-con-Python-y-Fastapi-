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

class Product_create(BaseModel):
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
    status: int
    category: int
    memory: int

class Product_update(BaseModel):
    name : Optional[str]
    price: Optional[float]
    description:Optional[str]
    track_inventory: Optional[bool]
    qty : Optional[int]
    width:Optional[float]
    weight: Optional[float]
    length: Optional[float]
    height: Optional[float]
    image_url : Optional[str] 
    seo_title :Optional[str]
    seo_desc :Optional[str]
    color: Optional[str]
    status: Optional[int]
    category: Optional[int]
    memory: Optional[int]

