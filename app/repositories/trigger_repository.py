from app.models.trigger_model import Trigger
from app.schemas.trigger_schemas import Trigger as TriggerSchema

from app.repositories.base_repository import BaseRepository


class TriggerRepository(BaseRepository):
    model: TriggerSchema = Trigger
