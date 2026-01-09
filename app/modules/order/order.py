from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from app.db import get_db
from sqlalchemy.orm import Session

from app.enum import OrderStatus
from app.models.models import Cart, Order, OrderProducts, Product
from app.schemas.schemas import OrderProduct, Order as SchemaOrder
from app.services.token import get_user_id_from_token

from app.exceptions import CustomException


def order_product(product: OrderProduct, db: Session = Depends(get_db)):
    stmt = select(Product).where(Product.id == product.id, Product.is_active == True)
    db_product = db.execute(stmt).scalar_one_or_none()
    if not db_product:
        raise CustomException(status_code=404, detail="Product not found")
    user_id = get_user_id_from_token()
    order = Order(
        user_id=user_id,
    )
    db.add(order)
    db.flush()
    order_product = OrderProducts(
        order_id=order.id,
        product_id=db_product.id,
        price=db_product.price,
        quantity=product.quantity,
    )
    db.add(order_product)
    db.commit()
    return {"message": "Order placed successfully"}


def order_cart(db: Session = Depends(get_db)):
    user_id = get_user_id_from_token()
    stmt = select(Cart).join(Product).where(Cart.user_id == user_id)
    db_cart = db.execute(stmt).scalars().all()
    if not db_cart:
        raise CustomException(status_code=422, detail={"message": "Cart not found"})
    order = Order(
        user_id=user_id,
    )
    db.add(order)
    db.flush()
    products: dict[UUID, Product] = {}
    for cart_item in db_cart:
        if not products[cart_item.product_id]:
            product_stmt = select(Product).where(
                Product.id == cart_item.product_id, Product.is_active == True
            )
            product = db.execute(product_stmt).scalar_one_or_none()
            if not product:
                raise CustomException(
                    status_code=422, data={"message": "Product is not available"}
                )
            products[product.id] = product
        order_product = OrderProducts(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=products[cart_item.product_id].price,
        )
        db.add(order_product)

    db.commit()
    return {"message": "Order placed successfully"}


def update_order_status(
    order_id: UUID, status: OrderStatus, db: Session = Depends(get_db)
):
    stmt = select(Order).where(Order.id == order_id)
    db_order = db.execute(stmt).scalar_one_or_none()
    if not db_order:
        raise CustomException(status_code=422, detail="Order not found")
    db_order.order_status = status
    db.commit()
    return {"message": "Order status updated successfully"}


def get_all_orders(db: Session = Depends(get_db)):
    stmt = select(Order).where(
        Order.user_id == get_user_id_from_token(), Order.is_active == True
    )
    db_orders = db.execute(stmt).scalars().all()
    return [SchemaOrder.model_validate(order.__dict__) for order in db_orders]
