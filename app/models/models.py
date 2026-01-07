from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Uuid,
    Enum,
)
from sqlalchemy.orm import relationship
from app.db import Base
from app.enum import UserType


class User(Base):
    __tablename__ = "users"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    type = Column(Enum(UserType), default=UserType.USER)


class Company(Base):
    __tablename__ = "companies"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, index=True)
    shop_id = Column(Uuid, ForeignKey("shops.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    shop = relationship("Shop", back_populates="companies")
    products = relationship("Product", back_populates="company")


class Shop(Base):
    __tablename__ = "shops"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    companies = relationship("Company", back_populates="shop")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, index=True)
    image = Column(String, nullable=True, default="")
    price = Column(Float, nullable=False, default=1)
    stock = Column(Integer, nullable=False, default=1)
    columns = Column(Integer, nullable=False, default=1)
    category_id = Column(Uuid, ForeignKey("categories.id"), nullable=False)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="products")
    company = relationship("Company", back_populates="products")
