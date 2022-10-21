from tokenize import String
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer, Float,String
from sqlalchemy import Table, Column, Integer, String, Float,ForeignKey
from config.db_config import meta,engine


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