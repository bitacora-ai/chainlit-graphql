from .endpoint import upload_routes
from .graphql import graphql_app

from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(upload_routes.router)
api_router.include_router(graphql_app.router, prefix="/graphql")
