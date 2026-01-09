from fastapi import APIRouter, Depends

from app.modules.export.export import export_company, export_shop
from app.services.token import validate_token


router = APIRouter(
    prefix="/export", tags=["Export"], dependencies=[Depends(validate_token)]
)


router.get("/company/{company_id}")(export_company)
router.get("/shop/{shop_id}")(export_shop)
