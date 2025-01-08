from sqlalchemy import Column, Integer, String, Float, Table
from ..database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


# Association table for many-to-many relationship between Order and Product
order_product_association = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    # Relationship with orders
    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    
    # Many-to-Many relationship with orders
    orders = relationship("Order",secondary=order_product_association,back_populates="products")



class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, default="Pending")  # Example: Pending, Completed, Canceled
    
    # Relationship with user
    user = relationship("User", back_populates="orders")
    
    # Many-to-Many relationship with products
    products = relationship("Product",secondary=order_product_association,back_populates="orders")

