from fastapi import APIRouter
from typing import List

from app.routers.dependencies import admin_service_dep
from app.schemas.controller_schemas import Controller
from app.schemas.device_schemas import Device
from app.schemas.trigger_schemas import Trigger
from app.schemas.user_schemas import SignUp, User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.post("/cr_user",response_model=User)
async def create_user(user_create: SignUp, user_service: admin_service_dep) -> User:
    user = await user_service.create_user(user_create)
    return user

@router.get("/get_users")
async def get_users(user_service: admin_service_dep):
    return await user_service.get_users()

@router.get("/get_devices", response_model=List[Device])
async def get_devices(device_service: admin_service_dep) -> List[Device]:
    return await device_service.get_devices()

@router.get("/get_triggers", response_model=List[Trigger])
async def get_triggers(trigger_service: admin_service_dep) -> List[Trigger]:
    return await trigger_service.get_triggers()

@router.get("/get_controllers", response_model=List[Controller])
async def get_controlers(controller_service: admin_service_dep) -> List[Trigger]:
    return await controller_service.get_triggers()