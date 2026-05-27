from fastapi import APIRouter
from pydantic import UUID4

from app.routers.dependencies import esp_service_dep
from app.schemas.esp_schemas import TriggerValueIn, TriggerValueOut, ControllerStateOut

router = APIRouter(
    prefix="/esp",
    tags=["ESP32"]
)

# ESP надсилає ping
@router.post("/device/{device_id}/ping")
async def device_ping(
        device_id: UUID4,
        esp_service: esp_service_dep):
    return await esp_service.ping_device(device_id)

@router.put("/trigger/{trigger_id}")
async def update_last_val(trigger_id: UUID4, esp_service: esp_service_dep, payload: TriggerValueIn):
    return await esp_service.update_last_val(trigger_id, payload)

@router.get("/controller/{controller_id}")
async def controller_state(
        controller_id: UUID4,
        esp_service: esp_service_dep):
    return await esp_service.get_controller_state(controller_id)
