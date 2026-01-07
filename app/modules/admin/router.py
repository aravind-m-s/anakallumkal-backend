from fastapi import APIRouter

from app.modules.admin.admin import create_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


router.post("/user/create")(create_user)
