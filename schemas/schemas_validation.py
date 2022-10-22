from typing import Optional
from pydantic import BaseModel


class Order (BaseModel):
    id: Optional[int]
    Sepal_longitud: float
    Sepal_ancho: float
    Petalo_longitud: float
    Petalo_ancho: float
    Especie: str