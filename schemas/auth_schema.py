from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        example="myemail@cosasdedevs.com"
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="MyTypicalUsername"
    )


class User(UserBase):
    # ... --> dato obligatorio
    id: int = Field(
        ...,
        example="5"
    )

# Modelo para registro de usuario
class UserRegister(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="strongpass"
    )

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None