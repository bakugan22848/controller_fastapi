import glob
import hashlib
import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import UUID4

from app.routers.dependencies import esp_service_dep
from app.schemas.esp_schemas import TriggerValueIn, TriggerValueOut, ControllerStateOut

router = APIRouter(
    prefix="/esp",
    tags=["ESP32"]
)

BUILDS_DIR = "C:/Users/ashna/PycharmProjects/ControllerBackEnd/builds"


@router.post("/device/{device_id}/build")
async def build_firmware(device_id: UUID4, esp_service: esp_service_dep):
    try:
        await esp_service.generate_firmware_for_device(device_id=device_id)
        return {
            "status": "success",
            "message": f"Прошивку для пристрою {device_id} успішно зкомпільовано та підготовлено до OTA."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка компіляції: {str(e)}"
        )


@router.get("/firmware/{device_id}/version")
async def get_firmware_version(device_id: UUID4, esp_service: esp_service_dep):
    # Шукаємо, який файл зараз лежить для цього UUID
    files = glob.glob(os.path.join(esp_service.builds_dir, f"{device_id}_*.bin"))
    if not files:
        return {"version": "v0"}

    # Витягуємо таймстамп з імені файлу
    version = os.path.basename(files[0]).replace(f"{device_id}_", "").replace(".bin", "")
    return {"version": version}


@router.get("/firmware/{device_id}")
async def get_firmware(device_id: UUID4, esp_service: esp_service_dep):
    files = glob.glob(os.path.join(esp_service.builds_dir, f"{device_id}_*.bin"))
    if not files:
        raise HTTPException(status_code=404, detail="Firmware not found")

    return FileResponse(path=files[0], media_type="application/octet-stream")


@router.put("/trigger/{trigger_id}")
async def update_last_val(trigger_id: UUID4, esp_service: esp_service_dep, payload: TriggerValueIn):
    return await esp_service.update_last_val(trigger_id, payload)

@router.get("/controller/{controller_id}")
async def controller_state(
        controller_id: UUID4,
        esp_service: esp_service_dep):
    return await esp_service.get_controller_state(controller_id)
