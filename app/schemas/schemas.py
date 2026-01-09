import datetime
from uuid import UUID
from pydantic import BaseModel

from app.enum import OrderStatus, PaymentStatus


class User(BaseModel):
    id: UUID
    name: str
    phone_number: str


class UserCreate(User):
    name: str
    phone_number: str
    password: str


class Login(BaseModel):
    phone_number: str
    password: str


class LoginResponse(Login):
    id: UUID
    access_token: str = ""

    class Config:
        from_attributes = True


class UserUpdate(UserCreate):
    password: str | None = None


class Shop(BaseModel):
    id: UUID
    name: str
    is_active: bool


class Category(BaseModel):
    id: UUID
    name: str
    is_active: bool


class Company(BaseModel):
    id: UUID
    name: str
    shop: Shop
    is_active: bool


class CreateShop(BaseModel):
    name: str


class CreateCategory(BaseModel):
    name: str


class CreateCompany(BaseModel):
    name: str
    shop_id: UUID


class Product(BaseModel):
    id: UUID
    name: str
    image: str
    price: float
    stock: int
    rows: int
    category: Category
    company: Company
    is_active: bool


class CreateProduct(BaseModel):
    name: str
    image: str
    price: float
    stock: int
    rows: int
    category_id: UUID
    company_id: UUID


class CartProduct(Product):
    quantity: int


class OrderProduct(BaseModel):
    product_id: UUID
    quantity: int


class Order(BaseModel):
    id: UUID
    order_number: int
    payment_status: PaymentStatus
    order_status: OrderStatus
    created_at: datetime.datetime
