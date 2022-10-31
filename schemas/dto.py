from typing import Optional, Union, List
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from typing import Optional


class AllOptional(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)

class Omit(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        omit_fields = getattr(namespaces.get("Config", {}), "omit_fields", {})
        fields = namespaces.get('__fields__', {})
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            fields.update(base.__fields__)
            annotations.update(base.__annotations__)
        merged_keys = fields.keys() & annotations.keys()
        [merged_keys.add(field) for field in fields]
        new_fields = {}
        new_annotations = {}
        for field in merged_keys:
            if not field.startswith('__') and field not in omit_fields:
                new_annotations[field] = annotations.get(field, fields[field].type_)
                new_fields[field] = fields[field]
        namespaces['__annotations__'] = new_annotations
        namespaces['__fields__'] = new_fields
        return super().__new__(self, name, bases, namespaces, **kwargs)

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

class ProductDTO(Product, metaclass=Omit):
    class Config:
        omit_fields = {'status_id','category_id','memory_id'}