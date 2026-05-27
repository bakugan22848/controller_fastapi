from fastapi import APIRouter, Depends
from pydantic import UUID4

from typing import List

from app.routers.dependencies import controller_service_dep, auth_service_dep
from app.schemas.controller_schemas import Controller, ControllerCreate, ControllerUpdate
from app.schemas.user_schemas import User

router = APIRouter(
    prefix="/controller",
    tags=["Controller"]
)

@router.post("/", response_model=Controller)
async def create_controller(controller_create: ControllerCreate, controller_service: controller_service_dep,
                            current_user: User = Depends(auth_service_dep.get_current_user)):
    return await controller_service.create_controller(controller_create, current_user.id)

@router.get("/", response_model=List[Controller])
async def get_controllers_by_device(device_id: UUID4, controller_service: controller_service_dep,
                                    current_user: User = Depends(auth_service_dep.get_current_user)):
    return await controller_service.get_controllers_by(device_id, current_user.id)

@router.get("/{controller_id}", response_model=Controller)
async def get_controller(controller_id: UUID4, controller_service: controller_service_dep,
                         current_user: User = Depends(auth_service_dep.get_current_user)):
    return await controller_service.get_controller(controller_id, current_user.id)

@router.put("/{controller_id}", response_model=Controller)
async def update_controller(controller_id: UUID4, controller: ControllerUpdate, controller_service: controller_service_dep,
                            current_user: User = Depends(auth_service_dep.get_current_user)):
    return await controller_service.update_controller(controller_id, current_user.id, controller)

@router.delete("/{controller_id}", response_model=Controller)
async def delete_controller(controller_id: UUID4, controller_service: controller_service_dep,
                            current_user: User = Depends(auth_service_dep.get_current_user)):
    return await controller_service.delete_controller(controller_id, current_user.id)