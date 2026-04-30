from app.models.controller_model import Controller
from app.schemas.controller_schemas import Controller as ControllerSchema

from app.repositories.base_repository import BaseRepository


class ControllerRepository(BaseRepository):
    model: ControllerSchema = Controller
