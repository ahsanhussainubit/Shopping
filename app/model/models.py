# Ensure the association tables are declared before the models
from sqlalchemy import Column, Integer, String, Float, Table, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

# Association table for many-to-many relationship between Order and Product
order_product_association = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)


# Models and relationships
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    # Relationship with orders
    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    img_url = Column(String, nullable=True)  # Changed to snake_case
    product_url = Column(String, nullable=True)  # Changed to snake_case
    stars = Column(Float, nullable=False)
    reviews = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    list_price = Column(Float, nullable=False)  # Changed to snake_case
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    is_best_seller = Column(Boolean, nullable=False)  # Changed to snake_case
    bought_in_last_month = Column(Integer, nullable=False)  # Changed to snake_case

    # Relationship with category
    category = relationship("Category", back_populates="products")
    # Many-to-Many relationship with orders
    orders = relationship("Order", secondary=order_product_association, back_populates="products")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationship with products
    products = relationship("Product", back_populates="category")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, default="Pending")  # Example: Pending, Completed, Canceled

    # Relationship with user
    user = relationship("User", back_populates="orders")

    # Many-to-Many relationship with products
    products = relationship("Product", secondary=order_product_association, back_populates="orders")
