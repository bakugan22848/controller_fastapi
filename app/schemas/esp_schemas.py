from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class TriggerValueIn(BaseModel):
    value: float

class TriggerValueOut(TunedModel):
    trigger_id: UUID4
    value: int
    notif_triggered: bool
    controller_state: Optional[bool] = None

class ControllerStateOut(TunedModel):
    controller_id: UUID4
    last_state: Optional[bool] = None
