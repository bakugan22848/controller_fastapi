from app.models.device_model import Device
from app.schemas.device_schemas import Device as DeviceSchema

from app.repositories.base_repository import BaseRepository


class DeviceRepository(BaseRepository):
    model: DeviceSchema = Device
