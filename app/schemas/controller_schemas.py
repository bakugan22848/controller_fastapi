from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, EmailStr, UUID4

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class Controller(TunedModel):
    id: UUID4
    name: str
    device_id: UUID4
    last_state: bool
    trigger_value: int
    created_at: datetime
    updated_at: datetime

class ControllerCreate(BaseModel):
    name: str
    device_id: UUID4
    trigger_value: int

class ControllerUpdate(BaseModel):
    name: str

class ControllerList(TunedModel):
    controllers: List[Controller]

class ControllerDetails(TunedModel):
    controller: Controller






