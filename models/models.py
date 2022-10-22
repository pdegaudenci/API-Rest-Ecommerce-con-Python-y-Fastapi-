from tokenize import String
from sqlalchemy.sql.sqltypes import Integer, Float,String,Date
from sqlalchemy import Column,ForeignKey
from config.db_config import engine, Base

"""Declaracion de clases que heredan de clase Base para que se pueda hacer el mapeo automatico Clase-->Tabla"""
class Customer(Base):
    __tablename__ = 'Customers'
    id_customer = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email =Column(String, nullable=False)
    billing_address = Column(String, nullable=False)
    default_shipping_address=Column(String, nullable=False)
    zip_code= Column(String, nullable=False)
    country= Column(String, nullable=False)
    phone =Column(String, nullable=False)
    
    def __init__(self, full_name,email,billing_address,default_shipping_address,zip_code,country,phone):
        self.full_name = full_name
        self.email = email
        self.billing_address=billing_address
        self.default_shipping_address= default_shipping_address
        self.zip_code=zip_code
        self.country=country
        self.phone=phone
    def __repr__(self):
        return f'Customer({self.full_name}, {self.billing_address})'
    def __str__(self):
        return self.full_name

class Order(Base):
    __tablename__ = 'Orders'
    id_order = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("Customers.id_customer"),nullable=False)
    total_ammount =Column(Float, nullable=False)
    shipping_address = Column(String, nullable=False)
    order_address=Column(String, nullable=False)
    order_email= Column(String, nullable=False)
    order_date= Column(Date, nullable=False)
    order_status =Column(String, nullable=False)
    
    def __init__(self, full_name,email,billing_address,default_shipping_address,zip_code,country,phone):
        self.full_name = full_name
        self.email = email
        self.billing_address=billing_address
        self.default_shipping_address= default_shipping_address
        self.zip_code=zip_code
        self.country=country
        self.phone=phone
    def __repr__(self):
        return f'Customer({self.full_name}, {self.billing_address})'
    def __str__(self):
        return self.full_name

Base.metadata.create_all(engine)
"""
from config.db_config import engine, Base,meta
from sqlalchemy import Table, Column, Integer, String, Float,ForeignKey
customers =Table("Customer", meta, 
    Column ("id_customer", Integer, primary_key= True),
    Column("full_name", String()),
    Column("email", String()),
    Column("billing_address", Float()),
    Column("default_shipping_address", Float()),
    Column("zip_code", String(40)),
    Column("country", String(40)),
    Column("phone", String(40))
    )

orders =Table("Orders", meta, 
    Column ("id_order", Integer, primary_key= True),
    Column("customer_id",Integer,ForeignKey("Customer.id_customer")),
    Column("total_ammount", String()),
    Column("shipping_address", Float()),
    Column("order_address", Float()),
    Column("order_email", String(40)),
    Column("order_date", String(40)),
    Column("order_status", String(40))
    )


meta.create_all(engine,checkfirst=True)
"""