import datetime
from typing import Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.exceptions import CustomException
from app.models.models import Shop, Shop
from app.schemas.schemas import (
    CreateShop,
    Shop as SchemaShop,
    Shop as SchemaShop,
    Shop as SchemaShop,
)

from app.db import get_db


def create_shop(shop: CreateShop, db: Session = Depends(get_db)):
    if shop.name.strip() == "":
        raise CustomException(status_code=422, detail="Shop name is required")
    shop = Shop(shop.model_dump())
    db.add(shop)
    db.commit()
    return {"message": "Shop created successfully"}


def get_shops(status: Optional[bool] = None, db: Session = Depends(get_db)):
    stmt = select(Shop).where(Shop.deleted_at == None)
    if status:
        stmt = stmt.where(Shop.is_active == status)
    shops = db.execute(stmt).scalars().all()
    return [SchemaShop.model_validate(shop.__dict__) for shop in shops]


def update_shop(shop_id: UUID, shop: CreateShop, db: Session = Depends(get_db)):
    db_shop = db.get(Shop, shop_id)
    if not db_shop:
        raise CustomException(status_code=422, detail="Shop not found")
    if shop.name.strip() == "":
        raise CustomException(status_code=422, detail="Shop name is required")
    db_shop.name = shop.name
    db.commit()
    return {"message": "Shop updated successfully"}


def delete_shop(shop_id: UUID, db: Session = Depends(get_db)):
    db_shop = db.get(Shop, shop_id)
    if not db_shop:
        raise CustomException(status_code=422, detail="Shop not found")
    db_shop.deleted_at = datetime.datetime.now()
    db.commit()
    return {"message": "Shop deleted successfully"}


def get_shop_products(shop_id: UUID, db: Session = Depends(get_db)):
    pass
