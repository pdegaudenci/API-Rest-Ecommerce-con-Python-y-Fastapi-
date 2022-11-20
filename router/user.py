from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from fastapi import Body
from fastapi import  Request,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from schemas import auth_schema
from services import auth_service,user_service
from schemas.auth_schema import Token
from schemas.auth_schema import User
from middleware.mw import get_current_user

user_router = APIRouter(prefix="/auth")

@user_router.post(
    "/user/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
def create_user(user: auth_schema.UserRegister = Body(...)):
    """
    ## Create a new user in the app

    ### Args
    The app can receive next fields into a JSON
    - email: A valid email
    - username: Unique username
    - password: Strong password for authentication

    ### Returns
    - user: User info
    """
    return user_service.create_user(user)

@user_router.post(
    "/login",
    tags=["users"],
    response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    ## Login for access token

    ### Args
    The app can receive next fields by form data
    - username: Your username or email
    - password: Your password

    ### Returns
    - access token and token type
    """
    access_token = auth_service.generate_token(form_data.username, form_data.password)
    return Token(access_token=access_token, token_type="bearer")

@user_router.get(path='/users',summary="Get all users", tags=["Customers && users"])   
def get_users(user: User = Depends(get_current_user)):
    response =[]
    if user.level=="admin":
        response = user_service.get_users()
        if len(response)==0:
            raise HTTPException(404,detail="No users found")
        response = JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK) 
    else :
        response = JSONResponse(content=jsonable_encoder({"response:":"No authorized method"}), status_code=status.HTTP_403_FORBIDDEN) 
    return response