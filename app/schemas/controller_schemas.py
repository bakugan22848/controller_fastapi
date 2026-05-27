from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, UUID4

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class Controller(TunedModel):
    id: UUID4
    name: str
    device_id: UUID4
    last_state: Optional[bool] = None
    trigger_value: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class ControllerCreate(BaseModel):
    name: str
    device_id: UUID4
    trigger_value: int

class ControllerUpdate(BaseModel):
    name: Optional[str] = None
    trigger_value: Optional[int] = None
    last_state: Optional[bool] = None

class ControllerList(TunedModel):
    controllers: List[Controller]

class ControllerDetails(TunedModel):
    controller: Controller






