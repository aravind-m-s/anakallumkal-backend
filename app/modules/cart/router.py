from fastapi import APIRouter, Depends

from app.modules.cart.cart import (
    add_product_to_cart,
    decrease_quantity,
    get_user_cart,
    increase_quantity,
    remove_product,
)
from app.services.token import validate_token

router = APIRouter(
    prefix="/cart", tags=["Cart"], dependencies=[Depends(validate_token)]
)

router.get("/{user_id}/list")(get_user_cart)
router.post("/{product_id}/add-product")(add_product_to_cart)
router.put("/{product_id}/increase-quantity")(increase_quantity)
router.put("/{product_id}/decrease-quantity")(decrease_quantity)
router.delete("/{product_id}/remove-product")(remove_product)
