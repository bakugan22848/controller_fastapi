from typing import List

from pydantic import BaseModel, Field, EmailStr, UUID4


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class TriggerData(TunedModel):
    trigger_id: UUID4
    value: int
    created_at: datetime


class AddTriggerData(BaseModel):
    trigger_id: UUID4
    value: int


class TriggerDataList(TunedModel):
    trigger_datas: List[TriggerData]


class TriggerDataDetail(TunedModel):
    trigger_data: ControllerData