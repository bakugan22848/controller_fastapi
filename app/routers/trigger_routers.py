from fastapi import APIRouter
from pydantic import UUID4

from typing import List

from app.routers.dependencies import trigger_service_dep
from app.schemas.trigger_schemas import Trigger, TriggerCreate, TriggerUpdate

router = APIRouter(
    prefix="/trigger",
    tags=["Trigger"]
)

@router.post("/")
async def create_trigger(trigger_create: TriggerCreate, trigger_service: trigger_service_dep) -> Trigger:
    trigger = await trigger_service.create_trigger(trigger_create)
    return trigger

@router.get("/", response_model=List[Trigger])
async def get_triggers(trigger_service: trigger_service_dep) -> List[Trigger]:
    return await trigger_service.get_triggers()

@router.get("/{trigger_id}", response_model=Trigger)
async def get_trigger(trigger_id: UUID4, trigger_service: trigger_service_dep) -> Trigger:
    return await trigger_service.get_trigger(trigger_id)

@router.get("/{device_id}", response_model=List[Trigger])
async def get_trigger_by(device_id: UUID4, controller_service: trigger_service_dep) -> List[Trigger]:
    return await controller_service.get_trigger_by(device_id)

@router.put("/{trigger_id}", response_model=Trigger)
async def update_trigger(trigger_id: UUID4, trigger: TriggerUpdate, trigger_service: trigger_service_dep) -> Trigger:
    trigger = await trigger_service.update_trigger(trigger_id, trigger)
    return trigger

@router.delete("/{trigger_id}", response_model=Trigger)
async def delete_trigger(trigger_id: UUID4, trigger_service: trigger_service_dep) -> Trigger:
    trigger = await trigger_service.delete_trigger(trigger_id)
    return trigger
