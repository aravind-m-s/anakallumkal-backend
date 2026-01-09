from fastapi import APIRouter, Depends

from app.modules.order.order import (
    get_all_orders,
    order_cart,
    order_product,
    update_order_status,
)
from app.services.token import validate_token


router = APIRouter(
    prefix="/order", tags=["Order"], dependencies=[Depends(validate_token)]
)


router.post("/order-product")(order_product)
router.post("/order-cart")(order_cart)
router.put("/update-order-status")(update_order_status)
router.get("/list")(get_all_orders)
