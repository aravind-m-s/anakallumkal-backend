from fastapi import APIRouter, Depends

from app.modules.admin.admin import create_user
from app.services.token import validate_token

router = APIRouter(
    prefix="/admin", tags=["Admin"], dependencies=[Depends(validate_token)]
)


router.post("/user/create")(create_user)
