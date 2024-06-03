from fastapi import APIRouter
from api.routes.cars import cars_router

router = APIRouter()

router.include_router(cars_router, prefix="/cars")
