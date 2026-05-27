from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, UUID4

class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class Trigger(TunedModel):
    id: UUID4
    name: str
    device_id: UUID4
    controller_id: Optional[UUID4]
    notif_state: Optional[bool] = None
    notif_value: Optional[int] = None
    last_value: Optional[int] = None
    check_clock: int
    write_clock: int
    created_at: datetime
    updated_at: datetime

class TriggerCreate(BaseModel):
    name: str
    device_id: UUID4
    controller_id: Optional[UUID4]
    notif_state: Optional[bool] = None
    notif_value: int
    check_clock: int
    write_clock: int

class TriggerUpdate(BaseModel):
    name: Optional[str] = None
    controller_id: Optional[UUID4] = None
    notif_state: Optional[bool] = None
    notif_value: Optional[int] = None
    check_clock: Optional[int] = None
    write_clock: Optional[int] = None

class TriggerList(TunedModel):
    triggers: List[Trigger]

class TriggerDetails(TunedModel):
    trigger: Trigger