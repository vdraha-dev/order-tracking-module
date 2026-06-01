from fastapi import Depends, status
from fastapi.routing import APIRouter

from app.users.api.v1.schemas import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
    UserLoginResponse,
)
from app.users.service import UserService, get_user_service

auth = APIRouter(prefix="/auth")


@auth.post(
    "/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    data = await user_service.create_user(user=user)
    return data


@auth.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def login(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    data = await user_service.handle_login(user)

    return data
