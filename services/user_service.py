from fastapi import HTTPException, status

from models.models import User as UserModel 
from schemas import auth_schema
from services.auth_service import get_password_hash
from config.db_config import session

def create_user(user: auth_schema.UserRegister):

    get_user = session.query(UserModel).filter((UserModel.email == user.email) | (UserModel.username == user.username)).first()
    if get_user:
        msg = "Email already registered"
        if get_user.username == user.username:
            msg = "Username already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )

    session.add(db_user)
    session.commit()

    return db_user