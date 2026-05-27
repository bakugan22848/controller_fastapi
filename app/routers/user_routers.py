from fastapi import APIRouter, Depends
from pydantic import UUID4


from app.routers.dependencies import user_service_dep, auth_service_dep
from app.schemas.user_schemas import  User, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(auth_service_dep.get_current_user),
                 user_service: user_service_dep = user_service_dep) -> User:
    return await user_service.get_user(current_user.id)

@router.put("/me", response_model=User)
async def update_user(user: UserUpdate, current_user: User = Depends(auth_service_dep.get_current_user),
                      user_service: user_service_dep =user_service_dep) -> User:
    updated_user = await user_service.update_user(current_user.id, user)
    return updated_user

@router.delete("/me", response_model=User)
async def delete_user(current_user: User = Depends(auth_service_dep.get_current_user),
                    user_service: user_service_dep = user_service_dep) -> User:
    user = await user_service.delete_user(current_user.id)
    return user