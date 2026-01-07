from fastapi import APIRouter

from app.modules.product.product import (
    create_product,
    delete_product,
    get_all_products,
    update_product,
)


router = APIRouter(
    prefix="/product",
    tags=["Product"],
)


router.post("/create")(create_product)
router.get("/list")(get_all_products)
router.put("/update/{product_id}")(update_product)
router.delete("/delete/{product_id}")(delete_product)
