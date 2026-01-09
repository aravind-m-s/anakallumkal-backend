from fastapi import FastAPI
from starlette.responses import JSONResponse
from app.exceptions import CustomException
from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.company.router import router as company_router
from app.modules.category.router import router as category_router
from app.modules.shop.router import router as shop_router
from app.modules.product.router import router as product_router
from app.modules.cart.router import router as cart_router
from app.modules.order.router import router as order_router
from app.modules.export.router import router as export_router


app = FastAPI(
    title="Anakallumkal API",
    description="Anakallumkal API",
    version="0.0.1",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none",
        "persistAuthorization": True,
    },
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(company_router)
app.include_router(category_router)
app.include_router(shop_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(export_router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    content = exc.data
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )
