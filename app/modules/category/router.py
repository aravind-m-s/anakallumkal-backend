from fastapi import APIRouter, Depends

from app.services.token import validate_token


from app.modules.category.category import (
    create_category,
    delete_category,
    get_categories,
    get_category_products,
    update_category,
)

router = APIRouter(
    prefix="/category", tags=["Category"], dependencies=[Depends(validate_token)]
)

router.post("/create")(create_category)
router.get("/list")(get_categories)
router.put("/update/{category_id}")(update_category)
router.delete("/delete/{category_id}")(delete_category)
router.get("/category-products/{category_id}")(get_category_products)
