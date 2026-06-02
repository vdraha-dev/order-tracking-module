from fastapi import Depends, status
from fastapi.routing import APIRouter

from app.users.api.v1.schemas import (
    UserCreate,
    UserCreateResponse,
)
from app.users.service import UserService, get_user_service

user = APIRouter(prefix="/user")


@user.post("/", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
):
    data = await service.create_user(user)
    return data
