from fastapi import APIRouter, Depends
from pydantic import UUID4

from typing import List

from app.routers.dependencies import device_service_dep, auth_service_dep


from app.schemas.device_schemas import Device, DeviceCreate, DeviceUpdate, DeviceWCount
from app.schemas.user_schemas import User

router = APIRouter(
    prefix="/device",
    tags=["Device"]
)

@router.post("/")
async def create_device(device_create: DeviceCreate,
                        device_service: device_service_dep,
                        current_user: User = Depends(auth_service_dep.get_current_user)) -> Device:
    device = await device_service.create_device(device_create, current_user.id)
    return device

@router.get("/", response_model=List[DeviceWCount])
async def get_my_devices(device_service: device_service_dep,
                         current_user: User = Depends(auth_service_dep.get_current_user)) -> List[DeviceWCount]:
    return await device_service.get_devices_by(current_user.id)

@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: UUID4,
                     device_service: device_service_dep,
                     current_user: User = Depends(auth_service_dep.get_current_user)) -> Device:
    return await device_service.get_device(device_id, current_user.id)


@router.put("/{device_id}", response_model=Device)
async def update_device(device_id: UUID4,
                        device: DeviceUpdate,
                        device_service: device_service_dep,
                        current_user: User = Depends(auth_service_dep.get_current_user)) -> Device:
    device = await device_service.update_device(device_id, current_user.id, device)
    return device


@router.delete("/{device_id}", response_model=Device)
async def delete_device(device_id: UUID4, device_service: device_service_dep,
                        current_user: User = Depends(auth_service_dep.get_current_user)) -> Device:
    device = await device_service.delete_device(device_id, current_user.id)
    return device