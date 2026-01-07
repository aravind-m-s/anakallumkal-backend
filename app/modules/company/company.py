import datetime
from typing import Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.exceptions import CustomException
from app.models.models import Category, Company, Shop
from app.schemas.schemas import (
    CreateCompany,
    Company as SchemaCompany,
    Shop as SchemaShop,
    Category as SchemaCategory,
)
from app.db import get_db


def create_company(company: CreateCompany, db: Session = Depends(get_db)):
    shop = db.get(Shop, company.shop_id)
    if company.name.strip() == "":
        raise CustomException(status_code=422, detail="Company name is required")
    if not shop:
        raise CustomException(status_code=422, detail="Shop not found")
    category = db.get(Category, company.category_id)
    if not category:
        raise CustomException(status_code=422, detail="Category not found")

    company = Company(company.model_dump())
    db.add(company)
    db.commit()
    return {"message": "Company created successfully"}


def get_companies(status: Optional[bool] = None, db: Session = Depends(get_db)):
    stmt = select(Company).join(Category).where(Company.deleted_at == None)
    if status:
        stmt = stmt.where(Company.is_active == status)
    companies = db.execute(stmt).scalars().all()
    return [
        SchemaCompany.model_validate(
            {
                **company.__dict__,
                "shop": SchemaShop.model_validate(company.shop.__dict__),
                "category": SchemaCategory.model_validate(company.category.__dict__),
            }
        )
        for company in companies
    ]


def update_company(
    company_id: UUID, company: CreateCompany, db: Session = Depends(get_db)
):
    db_company = db.get(Company, company_id)
    if not db_company:
        raise CustomException(status_code=422, detail="Company not found")
    shop = db.get(Shop, company.shop_id)
    if company.name.strip() == "":
        raise CustomException(status_code=422, detail="Company name is required")
    if not shop:
        raise CustomException(status_code=422, detail="Shop not found")
    category = db.get(Category, company.category_id)
    if not category:
        raise CustomException(status_code=422, detail="Category not found")

    db_company.name = company.name
    db_company.shop_id = company.shop_id
    db_company.category_id = company.category_id
    db.commit()
    return {"message": "Company updated successfully"}


def delete_company(company_id: UUID, db: Session = Depends(get_db)):
    db_company = db.get(Company, company_id)
    if not db_company:
        raise CustomException(status_code=422, detail="Company not found")
    db_company.deleted_at = datetime.datetime.now()
    db.commit()
    return {"message": "Company deleted successfully"}


def get_shop_companies(shop_id: UUID, db: Session = Depends(get_db)):
    stmt = select(Shop).join(Company).join(Category).where(Shop.id == shop_id)
    shop = db.execute(stmt).scalar_one_or_none()
    if not shop:
        raise CustomException(status_code=422, detail="Shop not found")

    companies = shop.companies
    return [
        SchemaCompany.model_validate(
            {
                **company.__dict__,
                "shop": SchemaShop.model_validate(company.shop.__dict__),
                "category": SchemaCategory.model_validate(company.category.__dict__),
            }
        )
        for company in companies
    ]


def get_company_products(company_id: UUID, db: Session = Depends(get_db)):
    pass
