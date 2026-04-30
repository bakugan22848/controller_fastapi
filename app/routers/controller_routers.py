from fastapi import APIRouter
from pydantic import UUID4

from typing import List

from app.routers.dependencies import controller_service_dep
from app.schemas.controller_schemas import Controller, ControllerCreate, ControllerUpdate

router = APIRouter(
    prefix="/controller",
    tags=["Controller"]
)

@router.post("/")
async def create_controller(controller_create: ControllerCreate, controller_service: controller_service_dep) -> Controller:
    controller = await controller_service.create_controller(controller_create)
    return controller

@router.get("/", response_model=List[Controller])
async def get_controllers(controller_service: controller_service_dep) -> List[Controller]:
    return await controller_service.get_controllers()

@router.get("/{device_id}", response_model=List[Controller])
async def get_controllers_by(device_id: UUID4, controller_service: controller_service_dep) -> List[Controller]:
    return await controller_service.get_controllers_by(device_id)

@router.get("/{controller_id}", response_model=Controller)
async def get_controller(controller_id: UUID4, controller_service: controller_service_dep) -> Controller:
    return await controller_service.get_controller(controller_id)

@router.put("/{controller_id}", response_model=Controller)
async def update_controller(controller_id: UUID4, controller: ControllerUpdate, controller_service: controller_service_dep) -> Controller:
    controller = await controller_service.update_controller(controller_id, controller)
    return controller

@router.delete("/{controller_id}", response_model=Controller)
async def delete_controller(controller_id: UUID4, controller_service: controller_service_dep) -> Controller:
    controller = await controller_service.delete_controller(controller_id)
    return controller