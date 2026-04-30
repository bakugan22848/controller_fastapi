from fastapi import APIRouter
from pydantic import UUID4

from typing import List

from app.routers.dependencies import user_service_dep
from app.schemas.user_schemas import SignUp, UserList, User, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/")
async def create_user(user_create: SignUp, user_service: user_service_dep) -> User:
    user = await user_service.create_user(user_create)
    return user

@router.get("/", response_model=List[User])
async def get_users(user_service: user_service_dep) -> List[User]:
    return await user_service.get_users()

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID4, user_service: user_service_dep) -> User:
    return await user_service.get_user(user_id)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: UUID4, user: UserUpdate, user_service: user_service_dep) -> User:
    user = await user_service.update_user(user_id, user)
    return user

@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: UUID4, user_service: user_service_dep) -> User:
    user = await user_service.delete_user(user_id)
    return user