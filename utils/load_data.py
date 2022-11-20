from sqlalchemy import create_engine #importing sqlalchemy engine to create engine for the database
import pandas as pd 
from config.config import settings
from config.db_config import session  
from models.models import User


CONECTION_URL = settings.DATABASE_URL
engine = create_engine(CONECTION_URL)

#Data of table memory Options
data = pd.read_excel('../data/Memory_options.xlsx')
data.to_sql('Memory_options', engine,if_exists='append',index=False)

# Product_categories
data = pd.read_excel('../data/Product_categories.xlsx')
data.to_sql('Product_categories', engine,if_exists='append',index=False)

#Status_options
data = pd.read_excel('../data/Status_options.xlsx')
data.to_sql('Status_options', engine,if_exists='append',index=False)

# Products
data = pd.read_excel('../data/Products.xlsx')
data.to_sql('Products', engine,if_exists='append',index=False)

# Creacion de usuario administrador
admin_user = User(settings.admin_user,settings.pwd_admin,None,"admin")
session.add(admin_user)
session.commit()
session.close()
