from app.models.trigger_data_model import TriggerData
from app.schemas.trigger_data_schemas import TriggerData as TriggerDataSchema

from app.repositories.base_repository import BaseRepository


class TriggerDataRepository(BaseRepository):
    model: TriggerDataSchema = TriggerData
