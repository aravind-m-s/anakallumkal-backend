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
from app.enum import OrderStatus, PaymentStatus, UserType


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

    cart = relationship("Cart", back_populates="user")
    order = relationship("Order", back_populates="user")


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
    product = relationship("Product", back_populates="company")


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

    product = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, index=True)
    image = Column(String, nullable=True, default="")
    price = Column(Float, nullable=False, default=1)
    stock = Column(Integer, nullable=False, default=1)
    rows = Column(Integer, nullable=False, default=1)
    category_id = Column(Uuid, ForeignKey("categories.id"), nullable=False)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="product")
    company = relationship("Company", back_populates="product")
    cart = relationship("Cart", back_populates="product")
    order_products = relationship("OrderProducts", back_populates="product")


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    product_id = Column(Uuid, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="cart")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    order_number = Column(Integer, default=0, autoincrement=True)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.ORDER_CONFIRMED)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="order")
    order_products = relationship("OrderProducts", back_populates="order")


class OrderProducts(Base):
    __tablename__ = "order_products"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    order_id = Column(Uuid, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Uuid, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")
