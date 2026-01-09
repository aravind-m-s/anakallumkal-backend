from fastapi import APIRouter, Depends

from app.modules.shop.shop import (
    create_shop,
    delete_shop,
    get_shops,
    get_shop_products,
    update_shop,
)
from app.services.token import validate_token

router = APIRouter(
    prefix="/shop", tags=["Shop"], dependencies=[Depends(validate_token)]
)

router.post("/create")(create_shop)
router.get("/list")(get_shops)
router.put("/update/{shop_id}")(update_shop)
router.delete("/delete/{shop_id}")(delete_shop)
router.get("/shop-products/{shop_id}")(get_shop_products)
