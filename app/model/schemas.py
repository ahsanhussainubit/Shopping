from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    sub: str
    network : str

    class Config:
        orm_mode = True
        from_attributes = True

class CreateUser(BaseModel):
    name: str
    email: str
    sub: str
    network : str

class ShowUser(User):
    id: int

# Category Pydantic Models
class CategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        from_attributes = True


class CreateCategory(CategoryBase):
    pass


class ShowCategoryProduct(CategoryBase):
    id: int
    products: List["ShowProduct"] = []  # Nested relationship with products

class ShowCategory(CategoryBase):
    id: int


class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    img_url: Optional[str] = None
    product_url: Optional[str] = None
    stars: float
    reviews: int
    list_price: float
    is_best_seller: bool
    bought_in_last_month: int

    class Config:
        orm_mode = True
        from_attributes = True

class ProductCreate(Product):
     category_id: int

class ShowProduct(Product):
    id: int
    category: ShowCategory

class OrderCreate(BaseModel):
    status: str = "Pending"
    product_ids: list[int] = []

class Order(BaseModel):
    user_id: int
    status: str
    products: list[ShowProduct] = []

    class Config:
        orm_mode = True
        from_attributes = True


class ShowOrder(Order):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class AuthRequest(BaseModel):
    token: str
    network: str
