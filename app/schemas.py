from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True

class ShowUser(User):
    id: int


class Product(BaseModel):
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True  # Tells Pydantic to read data as an ORM model (SQLAlchemy)
        from_attributes = True  

class ProductCreate(Product):
    pass

class ShowProduct(Product):
    id: int

class OrderCreate(BaseModel):
    user_id: int
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