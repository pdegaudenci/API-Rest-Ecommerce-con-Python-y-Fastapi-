from pydantic import BaseModel,Field,EmailStr
from typing import Optional
from schemas.order_validation import Customer

class User_request(BaseModel):
    email: str
    id_customer: int
    level:str


class User(BaseModel):
    email: EmailStr = Field(
        ...,
        example="myemail@examplecom"
    )

class User_Admin(BaseModel):
    email: str
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="password"
    )
    level : Optional[str]


# Modelo para registro de usuario --> Longitud minima de contraseña : 8 / maxima:64
class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="password" 
    )
    customer: Customer
#Data de respuesta cuando se solicita autenticacion : token de autenticación y el tipo de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

# Datos que se incluye en el token ,antes de generarlo
class TokenData(BaseModel):
    username: Optional[str] = None