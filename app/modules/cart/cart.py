from uuid import UUID

from sqlalchemy import select
from app.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from app.exceptions import CustomException
from app.models.models import Cart, Category, Company, Product
from app.schemas.schemas import (
    CartProduct,
    Company as SchemaCompany,
    Category as SchemaCategory,
)
from app.services.token import get_user_id_from_token


def get_user_cart(db: Session = Depends(get_db)):
    user_id: UUID = Depends(get_user_id_from_token)
    stmt = (
        select(Cart)
        .join(Product)
        .join(Category)
        .join(Company)
        .where(
            Cart.user_id == user_id,
            Cart.is_active == True,
            Cart.product.is_active == True,
        )
    )
    result = db.execute(stmt).scalars().all()
    return [
        CartProduct.model_validate(
            {
                **product.product.__dict__,
                "category": SchemaCategory.model_validate(
                    product.product.category.__dict__
                ),
                "company": SchemaCompany.model_validate(
                    product.product.company.__dict__
                ),
            }
        )
        for product in result
    ]


def add_product_to_cart(product_id: UUID, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token()
    stmt = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    cart_product = db.execute(stmt).scalar_one_or_none()
    if not cart_product:
        cart_product = Cart(user_id=user_id, product_id=product_id, quantity=0)
    cart_product.quantity += 1
    db.add(cart_product)
    db.commit()
    return {"message": "Product added to cart"}


def increase_quantity(product_id: UUID, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token()
    stmt = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise CustomException(
            status_code=422, data={"product_id": "Product does not exist"}
        )
    product.quantity += 1
    db.commit()
    return {"message": "Quantity increased successfully"}


def decrease_quantity(product_id: UUID, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token()
    stmt = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise CustomException(
            status_code=422, data={"product_id": "Product does not exist"}
        )
    product.quantity -= 1
    if product.quantity < 1:
        product.is_active = False
    db.commit()
    return {
        "message": f"Quantity {"decreased" if product.quantity > 0 else "removed" } successfully"
    }


def remove_product(product_id: UUID, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token()
    stmt = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise CustomException(
            status_code=422, data={"product_id": "Product does not exist"}
        )
    product.quantity = 0
    product.is_active = False
    db.commit()
    return {"message": "Product removed successfully"}
