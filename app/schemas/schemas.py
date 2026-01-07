from uuid import UUID
from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    name: str
    phone_number: str


class UserCreate(User):
    name: str
    phone_number: str
    password: str


class UserUpdate(UserCreate):
    password: str | None = None


class Shop(BaseModel):
    id: UUID
    name: str
    status: bool


class Category(BaseModel):
    id: UUID
    name: str
    status: bool


class Company(BaseModel):
    id: UUID
    name: str
    shop: Shop
    category: Category
    status: bool


class CreateShop(BaseModel):
    name: str


class CreateCategory(BaseModel):
    name: str


class CreateCompany(BaseModel):
    name: str
    shop_id: UUID
    category_id: UUID


class Product(BaseModel):
    id: UUID
    name: str
    image: str
    price: float
    stock: int
    columns: int
    category: Category
    company: Company
    status: bool


class CreateProduct(BaseModel):
    name: str
    image: str
    price: float
    stock: int
    columns: int
    category_id: UUID
    company_id: UUID
