from fastapi import APIRouter
from pydantic import UUID4

from typing import List

from app.routers.dependencies import device_service_dep
from app.schemas.device_schemas import Device, DeviceCreate, DeviceUpdate

router = APIRouter(
    prefix="/device",
    tags=["Device"]
)

@router.post("/")
async def create_device(device_create: DeviceCreate, device_service: device_service_dep) -> Device:
    device = await device_service.create_device(device_create)
    return device

@router.get("/", response_model=List[Device])
async def get_devices(device_service: device_service_dep) -> List[Device]:
    return await device_service.get_devices()

@router.get("/{user_id}", response_model=List[Device])
async def get_devices_by(user_id: UUID4, device_service: device_service_dep) -> List[Device]:
    return await device_service.get_devices_by(user_id)

@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: UUID4, device_service: device_service_dep) -> Device:
    return await device_service.get_device(device_id)

@router.put("/{device_id}", response_model=Device)
async def update_device(device_id: UUID4, device: DeviceUpdate, device_service: device_service_dep) -> Device:
    device = await device_service.update_device(device_id, device)
    return device

@router.delete("/{device_id}", response_model=Device)
async def delete_device(device_id: UUID4, device_service: device_service_dep) -> Device:
    device = await device_service.delete_device(device_id)
    return device