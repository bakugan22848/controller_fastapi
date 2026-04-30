from app.models.controller_data_model import ControllerData
from app.schemas.controller_data_schemas import ControllerData as ControllerDataSchema

from app.repositories.base_repository import BaseRepository


class ControllerDataRepository(BaseRepository):
    model: ControllerDataSchema = ControllerData
