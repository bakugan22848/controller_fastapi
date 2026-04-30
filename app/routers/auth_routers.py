from fastapi import Depends, APIRouter

from app.routers.dependencies import auth_service_dep
from app.schemas.auth_schemas import TokenInfo
from app.schemas.user_schemas import SignUp,SignIn, User
from app.services.auth_service import AuthService

router = APIRouter(prefix="/jwt",tags=["JWT"])

@router.post("/signup", response_model=TokenInfo)
async def create_user(user_create: SignUp, service: auth_service_dep):
    return await service.sign_up(user_create)

@router.post("/signin", response_model=TokenInfo)
async def login_jwt(login_data: SignIn, service: auth_service_dep):
    return await service.sign_in(login_data)

@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(auth_service_dep.get_current_user)):
    return current_user