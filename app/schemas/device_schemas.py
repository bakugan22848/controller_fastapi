from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, EmailStr, UUID4

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class Device(TunedModel):
    id:UUID4
    name: str
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

class DeviceWCount(TunedModel):
    id:UUID4
    name: str
    user_id: UUID4
    periph_count: int
    created_at: datetime
    updated_at: datetime

class DeviceCreate(BaseModel):
    name: str

class DeviceUpdate(BaseModel):
    name: str

class DeviceList(TunedModel):
    devices: List[Device]

