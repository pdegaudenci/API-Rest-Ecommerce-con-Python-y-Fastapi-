from fastapi import HTTPException, status

from models.models import User ,Customer
from schemas import auth_schema
from services.auth_service import get_password_hash
from config.db_config import session
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

def update_user(user,email):
    try:
        if email !=None:
            session.query(User).filter(User.email == user.email).update({'email':email})
            session.commit()
    except: 
            session.rollback()
            session.close()
            raise HTTPException(404, detail='User Transaction Error / It was not updated ')
     # Recupera de la BBDD el producto actualizado y lo retorna como respuesta
    return get_user(email)

def create_customer(customer):
    respuesta = None
    obj = session.query(Customer).order_by(Customer.id_customer.desc()).first()
    if obj == None:
      new_id = 1
    else:
      new_id =obj.id_customer +1
    if verify_customer(customer.email) == True :
      respuesta = session.query(Customer).filter(Customer.email == customer.email).first()
    else:
      new_customer = Customer(new_id,customer.full_name,customer.email,customer.billing_address,customer.default_shipping_address,customer.zip_code,customer.country,customer.phone)
     # Ejecuto transaccion para agregar el cliente 
      try:
          # Agregar cliente
          session.add(new_customer)    
          #Ejecutar transaccion con varias operaciones y al hacer commit se ejecutarian como una sola unidad sobre la base de datos)
          session.commit()
          respuesta = new_customer
          respuesta = get_customer(customer)
      except: 
            # En caso que no se pueda ejecutar la insercion, hago rollback de la trasaccion y lanzo un HttpException
            logger.error('Error en base de datos creando customer con email %s',new_customer.email)
            session.rollback()
            raise HTTPException(404, detail='Transaction Error customer')
    # Recupera de la BBDD el cliente creado y lo retorna como respuesta
    return respuesta

def verify_customer(email):
    customer_exist = False
    if session.query(Customer).filter(Customer.email == email).first() != None:
      customer_exist = True
    return customer_exist  

def get_customer(user):
  result = session.query(Customer).filter(Customer.email == user.email).first()
  return result

def get_customers():
    return session.query(Customer).all()

def update_customer(customer, user):
    try:
        if customer !=None:
            session.query(Customer).filter(Customer.user== user.email).update(customer)
            session.commit()
            session.close()
    except: 
            session.rollback()
            session.close()
            raise HTTPException(404, detail='User Transaction Error / It was not updated ')
    return customer

def delete_user(email):
    result=False
    try:
        session.query(User).filter(User.email== email).delete()
        session.commit()
        result=True
    except: 
        session.rollback()
        session.close()
        raise HTTPException(500, detail='User Transaction Error / It was not deleted ')
    return result


def update_customerbyid(id,customer):
    try:
        if customer !=None:
            session.query(Customer).filter(Customer.id_customer == id).update(customer)
            session.commit()
    except: 
            session.rollback()
            session.close()
            raise HTTPException(404, detail='CustomerTransaction Error / Customer was not updated ')
    return customer

def get_customerbyemail(email):
    try:
            customer = session.query(Customer).filter(Customer.email == email).first()
            session.commit()
    except: 
            session.rollback()
            session.close()
            raise HTTPException(404, detail='CustomerTransaction Error / Customer not found')
    return customer