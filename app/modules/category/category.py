import datetime
from typing import Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.exceptions import CustomException
from app.models.models import Category, Shop
from app.schemas.schemas import (
    CreateCategory,
    Category as SchemaCategory,
    Shop as SchemaShop,
    Category as SchemaCategory,
)

from app.db import get_db


def create_category(category: CreateCategory, db: Session = Depends(get_db)):
    if category.name.strip() == "":
        raise CustomException(status_code=422, detail="Category name is required")
    category = Category(**category.model_dump())
    db.add(category)
    db.commit()
    return {"message": "Category created successfully"}


def get_categories(status: Optional[bool] = None, db: Session = Depends(get_db)):
    stmt = select(Category).where(Category.deleted_at == None)
    if status:
        stmt = stmt.where(Category.is_active == status)
    categories = db.execute(stmt).scalars().all()
    return [SchemaCategory.model_validate(category.__dict__) for category in categories]


def update_category(
    category_id: UUID, category: CreateCategory, db: Session = Depends(get_db)
):
    db_category = db.get(Category, category_id)
    if not db_category:
        raise CustomException(status_code=422, detail="Category not found")
    if category.name.strip() == "":
        raise CustomException(status_code=422, detail="Category name is required")
    db_category.name = category.name
    db.commit()
    return {"message": "Category updated successfully"}


def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    db_category = db.get(Category, category_id)
    if not db_category:
        raise CustomException(status_code=422, detail="Category not found")
    db_category.deleted_at = datetime.datetime.now()
    db.commit()
    return {"message": "Category deleted successfully"}


def get_category_products(category_id: UUID, db: Session = Depends(get_db)):
    pass
