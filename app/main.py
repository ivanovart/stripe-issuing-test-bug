from urllib.request import Request

import stripe.error
from fastapi import FastAPI
from fastapi.responses import JSONResponse


from app.api import router
from app.config import settings
from app.errors import CustomHTTPException

app = FastAPI(title="Stripe Bug Example", openapi_url=f"/openapi.json")


stripe.api_key = settings.STRIPE_API_KEY


async def custom_exception_handler(_request: Request, exc: CustomHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail},)

app.add_exception_handler(CustomHTTPException, custom_exception_handler)
app.include_router(router)
