from fastapi import APIRouter, Depends

from app.modules.company.company import (
    create_company,
    delete_company,
    get_companies,
    get_company_products,
    get_shop_companies,
    update_company,
)
from app.services.token import validate_token

router = APIRouter(
    prefix="/company", tags=["Company"], dependencies=[Depends(validate_token)]
)

router.post("/create")(create_company)
router.get("/list")(get_companies)
router.put("/update/{company_id}")(update_company)
router.delete("/delete/{company_id}")(delete_company)
router.get("/shop-company-list/{shop_id}")(get_shop_companies)
router.get("/company-products/{company_id}")(get_company_products)
