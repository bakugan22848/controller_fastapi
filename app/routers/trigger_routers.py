from fastapi import APIRouter, Depends
from pydantic import UUID4

from typing import List

from app.routers.dependencies import trigger_service_dep, auth_service_dep
from app.schemas.trigger_schemas import Trigger, TriggerCreate, TriggerUpdate
from app.schemas.user_schemas import User

router = APIRouter(
    prefix="/trigger",
    tags=["Trigger"]
)

@router.post("/")
async def create_trigger(trigger_create: TriggerCreate, trigger_service: trigger_service_dep,
                         current_user: User = Depends(auth_service_dep.get_current_user)) -> Trigger:
    trigger = await trigger_service.create_trigger(trigger_create, current_user.id)
    return trigger

@router.get("/{trigger_id}", response_model=Trigger)
async def get_trigger(trigger_id: UUID4, trigger_service: trigger_service_dep,
                         current_user: User = Depends(auth_service_dep.get_current_user)) -> Trigger:
    return await trigger_service.get_trigger(trigger_id, current_user.id)

@router.get("s/{device_id}", response_model=List[Trigger])
async def get_triggers_by_device(device_id: UUID4, trigger_service: trigger_service_dep,
                         current_user: User = Depends(auth_service_dep.get_current_user)) -> List[Trigger]:
    return await trigger_service.get_triggers_by(device_id, current_user.id)

@router.put("/{trigger_id}", response_model=Trigger)
async def update_trigger(trigger_id: UUID4, trigger: TriggerUpdate, trigger_service: trigger_service_dep,
                         current_user: User = Depends(auth_service_dep.get_current_user)) -> Trigger:
    trigger = await trigger_service.update_trigger(trigger_id, current_user.id, trigger)
    return trigger

@router.delete("/{trigger_id}", response_model=Trigger)
async def delete_trigger(trigger_id: UUID4, trigger_service: trigger_service_dep,
                         current_user: User = Depends(auth_service_dep.get_current_user)) -> Trigger:
    trigger = await trigger_service.delete_trigger(trigger_id, current_user.id)
    return trigger