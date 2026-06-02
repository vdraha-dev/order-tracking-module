from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(max_length=256)


class UserCreate(UserBase): ...


class UserCreateResponse(BaseModel):
    id: int
    username: str
