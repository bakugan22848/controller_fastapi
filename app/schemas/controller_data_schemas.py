from typing import List

from pydantic import BaseModel, Field, EmailStr, UUID4

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ControllerData(TunedModel):
    controller_id: UUID4
    state: bool
    created_at: datetime

class AddControllerData(BaseModel):
    controller_id: UUID4
    state: bool

class ControllerDataList(TunedModel):
    controller_datas: List[ControllerData]

class ControllerDataDetail(TunedModel):
    controller_data: ControllerData