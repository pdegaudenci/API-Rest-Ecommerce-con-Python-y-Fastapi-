from tokenize import String
from sqlalchemy.sql.sqltypes import Integer, Float,String,Date,Boolean
from sqlalchemy import Column,ForeignKey, Table,UniqueConstraint
from sqlalchemy.orm import  relationship

from config.db_config import engine, Base


"""Declaracion de clases que heredan de clase Base para que se pueda hacer el mapeo automatico Clase-->Tabla"""

class Customer(Base):
    __tablename__ = 'Customers'
    id_customer = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email =Column(String, nullable=False, unique=True)
    billing_address = Column(String, nullable=False)
    default_shipping_address=Column(String, nullable=False)
    zip_code= Column(String, nullable=False)
    country= Column(String, nullable=False)
    phone =Column(String, nullable=False)
    order= relationship("Order",back_populates="customer")
    def __init__(self,id, full_name,email,billing_address,default_shipping_address,zip_code,country,phone):
        self.id_customer = id
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


# Creacion de tabla intermedia para relacion many to many de productos y orders , incluyendo los atributos de la relacion
products_orders= Table('products_orders', Base.metadata,

    Column('order_id', Integer, ForeignKey('Orders.id_order')),
    Column('product_id', Integer, ForeignKey('Products.sku')),
    UniqueConstraint("order_id", "product_id"),
    Column('quantity',Integer,nullable=False),
    Column('payment_method',String,nullable=False)
)

class Product_Order(Base):
    __table__ = products_orders
    __mapper_args__ = {"primary_key": [products_orders.c.order_id, products_orders.c.product_id]}
    order_id = products_orders.c.order_id
    product_id = products_orders.c.product_id
    qty = products_orders.c.quantity
    payment =products_orders.c.payment_method

    def __init__(self,order_id,product_id,qty,payment):
        self.order_id = order_id
        self.product_id=product_id
        self.qty=qty
        self.payment=payment

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
    # RElacion muchos a muchos con productos
    customer= relationship("Customer",back_populates="order")
    products = relationship('Product', secondary=products_orders,back_populates='order')
    def __init__(self, id_order,customer_id,total_ammount,shipping_address,order_address,order_email,order_date,order_status):
       self.id_order=id_order
       self.customer= customer_id
       self.total_ammount= total_ammount
       self.shipping_address=shipping_address
       self.order_address=order_address
       self.order_email= order_email
       self.order_date= order_date
       self.order_status=order_status
    def __repr__(self):
        return f'Order({self.total_ammount}- {self.order_address} - {self.order_email})'
    def __str__(self):
        return self.id_order



class Status(Base):
    __tablename__ = 'Status_options'
    id_status = Column(Integer, primary_key=True)
    status_type = Column(String, nullable=False)

    products= relationship("Product",back_populates="status_product")

    def __init__(self,status_type):
        self.status_type=status_type

    def __repr__(self):
        return f'status({self.status_type})'
    def __str__(self):
        return self.status_type

class Categories(Base):
    __tablename__ = 'Product_categories'
    id_category = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    products= relationship("Product",back_populates="category_product")

    def __init__(self,name,description):
        self.name=name
        self.description=description

    def __repr__(self):
        return f'category({self.name})'
    def __str__(self):
        return self.name

class Memory(Base):
    __tablename__ = 'Memory_options'
    id_memory = Column(Integer, primary_key=True)
    memory_capacity = Column(Integer, nullable=False)
    capacity_type = Column(String, nullable=False)

    #Relacion con clase Product - atributo memory_product
    products= relationship("Product",back_populates="memory_product")

    def __init__(self,memory_capacity,capacity_type):
        self.memory_capacity=memory_capacity
        self.capacity_type= capacity_type

    def __repr__(self):
        return f'memory({self.memory_capacity}, {self.capacity_type})'
    def __str__(self):
        return self.memory_capacity



class Product(Base):
    __tablename__ = 'Products'
    sku = Column(Integer, primary_key=True,autoincrement=True)
    name= Column(String, nullable=False)
    price= Column(Float, nullable=False)
    description=Column(String, nullable=False)
    track_inventory = Column(Boolean,nullable=False)
    qty = Column(Integer, nullable=False)
    weight=Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    length =  Column(Float, nullable=False)
    image_url =Column(String)
    seo_title = Column(String, nullable=False)
    seo_desc= Column(String, nullable=False)
    color = Column(String, nullable=False)

    # Foreign Keys --> Relacion 1 a muchos
    status_id = Column(Integer, ForeignKey("Status_options.id_status"),nullable=False)
    category_id = Column(Integer, ForeignKey("Product_categories.id_category"),nullable=False)
    memory_id = Column(Integer, ForeignKey("Memory_options.id_memory"),nullable=False)
    status_product =relationship("Status", back_populates="products")
    memory_product =relationship("Memory", back_populates="products")
    category_product = relationship("Categories", back_populates="products")
    # Relacion many to may
    order = relationship('Order', secondary=products_orders,back_populates='products')
    
    def __init__(self,sku,name,price,description,track_inventory,qty,weight,height,width,length,image_url,seo_title,seo_desc,color,status_id,category_id,memory_id):
        self.sku=sku
        self.name= name
        self.price= price
        self.description = description
        self.track_inventory=track_inventory
        self.qty=qty
        self.weight=weight
        self.height=height
        self.image_url=image_url
        self.seo_title=seo_title
        self.seo_desc=seo_desc
        self.color=color
        self.status_id=status_id
        self.category_id= category_id
        self.memory_id=memory_id
        self.width=width
        self.length=length

    def __repr__(self):
        return f'product({self.name},{self.price},{self.description})'
    def __str__(self):
        return self.name



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