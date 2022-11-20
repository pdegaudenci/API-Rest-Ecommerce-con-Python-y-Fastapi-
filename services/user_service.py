from fastapi import HTTPException, status

from models.models import User ,Customer
from schemas import auth_schema
from services.auth_service import get_password_hash
from config.db_config import session
from services.orders_service import create_customer,verify_customer
from utils.logger import logger


def create_user_admin(user: auth_schema.User_Admin):
    # Verificar si usuario existe por email
    get_user = session.query(User).filter(User.email == user.email).first()
    if get_user:
        msg = "Email already registered"
        if get_user.email == user.email:
            msg = "Username already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
    try:
        #Crear usuario nuevo
        db_user = User(email=user.email,password=get_password_hash(user.password),id_customer=None,level="admin")
        session.add(db_user)
        session.commit()
        logger.warn('Creado usuario admnistrador --> %s',db_user.email)
    except:
        session.rollback()
        session.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error ocurrer creating a new user"
        ) 
    
    return auth_schema.User(
        email = db_user.email
    )

def create_user(user: auth_schema.UserRegister):
    session.rollback()
    # Verificar si usuario existe por email
    get_user = session.query(User).filter(User.email == user.email).first()
    if get_user:
        msg = "Email already registered"
        if get_user.email == user.email:
            msg = "Username already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
    # Verificar si existe cliente con ese email
    exist_customer = verify_customer(user.email)
    if exist_customer :
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An customer with same email already exists"
        )
    #Crear cliente
    customer = create_customer(user.customer)
    try:
        #Crear usuario nuevo
        db_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        id_customer=customer.id_customer
        )
        session.add(db_user)
        session.commit()
    except:
        session.rollback()
        session.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error ocurrer creating a new user"
        ) 
    
    return auth_schema.User(
        email = db_user.email
    )

def get_users():
    result = session.query(User).all() 
    lista =[]
    for user in result:
        result_user =auth_schema.User_request(email = user.email,id_customer=user.id_customer,level=user.level)
        lista.append(result_user)
    return lista

def get_user(email):
    return session.query(User).filter(User.email==email).first()

def delete_user(email):
    return session.query(User).filter(User.email==email).delete()

