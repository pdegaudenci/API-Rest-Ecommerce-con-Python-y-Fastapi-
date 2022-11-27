from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from models.models import User
from schemas.auth_schema import TokenData
from config.db_config import settings
from config.db_config import session


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Usa metodo verify de CryptContext para verificarpassword en texto plano con password en hash
def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

# Obtiene hash de password en texto plano pasado por parametro
def get_password_hash(password):
    return pwd_context.hash(password)

# Busca usuario en base de datos
def get_user(username: str):
    return session.query(User).filter(User.email == username).first()

# Verifica que exista usuario
# Compara hash de contraseña almacenada en BBDD con contraseña suministrada en peticion 
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_token(username, password):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    return create_access_token(
        data={"sub": user.email, "level": user.level}, expires_delta=access_token_expires
    )

def reset_password(user,password):
    result = True
    try:
        passw= get_password_hash(password)
        session.query(User).filter(User.email==user.email).update({'password':passw})
        session.commit()
    except:
        result = False
        session.rollback()
        session.close()
        raise HTTPException(500, detail='User Transaction Error / password was not updated ')
    return result