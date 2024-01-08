from fastapi import APIRouter

from api.endpoints import expense, users

api_router = APIRouter()

api_router.include_router(expense.router, prefix="/api", tags=["expense"])
api_router.include_router(users.router, prefix="/api", tags=["user"])