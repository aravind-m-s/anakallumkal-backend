import datetime
from typing import Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import Category, Company, Product
from app.schemas.schemas import CreateProduct, Product as SchemaProduct
from app.exceptions import CustomException


def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    if product.name.strip() == "":
        raise CustomException(
            status_code=422, data={"name": "Product name cannot be empty"}
        )
    if product.price <= 0:
        raise CustomException(
            status_code=422, data={"price": "Product price should be greater than 0"}
        )

    if product.stock < 0:
        raise CustomException(
            status_code=422, data={"stock": "Product stock cannot be negative"}
        )

    category = db.get(Category, product.category_id)
    if not category:
        raise CustomException(
            status_code=422, data={"category_id": "Invalid category id"}
        )

    company = db.get(Company, product.company_id)
    if not company:
        raise CustomException(
            status_code=422, data={"company_id": "Invalid company id"}
        )

    db.add(Product(**product.model_dump()))
    db.commit()
    return {"message": "Product created successfully"}


def get_all_products(status: Optional[bool] = None, db: Session = Depends(get_db)):
    stmt = select(Product).where(Product.deleted_at == None)
    if status is not None:
        stmt = stmt.where(Product.status == status)
    products = db.execute(stmt).scalars().all()
    return [SchemaProduct.model_validate(product.__dict__) for product in products]


def update_product(
    product_id: UUID, product: CreateProduct, db: Session = Depends(get_db)
):
    if product.name.strip() == "":
        raise CustomException(
            status_code=422, data={"name": "Product name cannot be empty"}
        )
    if product.price <= 0:
        raise CustomException(
            status_code=422, data={"price": "Product price should be greater than 0"}
        )

    if product.stock < 0:
        raise CustomException(
            status_code=422, data={"stock": "Product stock cannot be negative"}
        )

    category = db.get(Category, product.category_id)
    if not category:
        raise CustomException(
            status_code=422, data={"category_id": "Invalid category id"}
        )

    company = db.get(Category, product.company_id)
    if not company:
        raise CustomException(
            status_code=422, data={"company_id": "Invalid company id"}
        )
    db_product = db.get(Product, product_id)
    if not db_product:
        raise CustomException(
            status_code=422, data={"product_id": "Invalid product id"}
        )

    db_product.name = product.name
    db_product.image = product.image
    db_product.price = product.price
    db_product.stock = product.stock
    db_product.rows = product.rows
    db_product.category_id = product.category_id
    db_product.company_id = product.company_id

    db.commit()
    return {"message": "Product updated successfully"}


def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    db_product = db.get(Product, product_id)
    if not db_product:
        raise CustomException(
            status_code=422, data={"product_id": "Invalid product id"}
        )
    db_product.deleted_at = datetime.datetime.now()
    db.commit()
    return {"message": "Product deleted successfully"}
