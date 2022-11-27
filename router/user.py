from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from fastapi import Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from schemas import auth_schema,order_validation
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
    return user_service.create_user(user)

@user_router.post(
    "/login",
    tags=["users"],
    response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
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

@user_router.get(path='/user/{id}',summary="Get user by email", tags=["Customers && users"])   
def get_user(email:str,user: User = Depends(get_current_user)):
    response =[]
    if user.level=="admin" or user.email == email:
        response = user_service.get_user(email)
        response = JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK) 
    else :
        response = JSONResponse(content=jsonable_encoder({"response:":"No authorized method"}), status_code=status.HTTP_403_FORBIDDEN) 
    return response



@user_router.post(
    "/user/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
def create_user(user: auth_schema.UserRegister = Body(...)):
    return user_service.create_user(user)

@user_router.put(
    "/user/reset_pwd",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    summary="reset passwd of current user"
)
def reset_passwd(password:str,user: User = Depends(get_current_user)):
    response= auth_service.reset_password(user,password)
    if response==True:
        response =  JSONResponse(content=jsonable_encoder({"response:":"password was updated succesfully"}), status_code=status.HTTP_200_OK) 
    else:
        response=JSONResponse(content=jsonable_encoder({"response:":"password was not updated"}), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    return response

@user_router.delete(
    "/user/{id}",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    summary="delete user"
)
def delete_user(email_user:str,user: User = Depends(get_current_user)):
    if user.level =="admin" or email_user == user.email:
        response =user_service.delete_user(email_user)
        if response == True:
            response = JSONResponse(content=jsonable_encoder({"response:":"user was deleted succesfully"}), status_code=status.HTTP_200_OK) 
    else:
        raise HTTPException(403,detail="Forbiden")
    return response

@user_router.put(
    "/user/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    summary="update email user"
)
def update_user(email_user:str,user: User = Depends(get_current_user)):
    user_service.update_user(user,email_user)
    response = JSONResponse(content=jsonable_encoder({"response:":"user was update succesfully"}), status_code=status.HTTP_200_OK) 
    return response

@user_router.put(
    "/user/customer",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    summary="update email user"
)
def update_customer(customer:order_validation.Customer,user: User = Depends(get_current_user)):
    user_service.update_customer(customer,user)
    response = JSONResponse(content=jsonable_encoder({"response:":"customer data was update succesfully"}), status_code=status.HTTP_200_OK) 
    return response

@user_router.put(
    "/user/customer",
    tags=["Customers && users"],
    status_code=status.HTTP_200_OK,
    summary="update customer data"
)
def update_customerbyid(id:int,customer:order_validation.Customer,user: User = Depends(get_current_user)):
    if user.level =="admin":
        user_service.update_customerbyid(id,customer)
        response = JSONResponse(content=jsonable_encoder({"response:":"customer data was update succesfully"}), status_code=status.HTTP_200_OK) 
    else:
         raise HTTPException(403,detail="Forbiden")
    return response


@user_router.get(path='/customer',summary="Get customer", tags=["Customers && users"])   
def get_customer(email:str,user: User = Depends(get_current_user)):
    response =[]
    if user.level=="admin":
        response = user_service.get_customerbyemail(email)
        response = JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK) 
    else :
        response = JSONResponse(content=jsonable_encoder({"response:":"No authorized method"}), status_code=status.HTTP_403_FORBIDDEN) 
    return response

