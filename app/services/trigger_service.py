from datetime import datetime

from typing import List

from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.device_repository import DeviceRepository
from app.schemas.trigger_schemas import Trigger, TriggerCreate, TriggerUpdate
from app.repositories.trigger_repository import TriggerRepository


class TriggerService:
    def __init__(self, session: AsyncSession, repository: TriggerRepository, device_repository: DeviceRepository):
        self.session = session
        self.repository = repository
        self.device_repository = device_repository


    async def create_trigger(self, data: TriggerCreate, user_id: UUID4) -> Trigger:
        try:

            device = await self.device_repository.get_one(id=data.device_id)
            if not device:
                raise HTTPException(status_code=404, detail="Device not found")
            if device.user_id != user_id:
                raise HTTPException(status_code=403, detail="Access denied")

            trigger_data = {
                "name": data.name,
                "device_id": data.device_id,
                "notif_state": data.notif_state,
                "notif_value": data.notif_value,
                "type": data.type,
                "pin": data.pin
            }

            trigger = await self.repository.create_one(trigger_data)
            await self.session.commit()
            return Trigger.model_validate(trigger)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't connect trigger"
            )

    async def get_triggers_by(self, device_id: UUID4, user_id: UUID4) -> List[Trigger]:
        device = await self.device_repository.get_one(id=device_id)

        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        if device.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        triggers = await self.repository.get_many_by(device_id=device_id)
        return triggers

    async def get_trigger(self, trigger_id: UUID4, user_id: UUID4) -> Trigger:
        trigger = await self.repository.get_one(id=trigger_id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")

        device = await self.device_repository.get_one(id=trigger.device_id)
        if device.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        return Trigger.model_validate(trigger)

    async def update_trigger(self, trigger_id: UUID4, user_id: UUID4,  data: TriggerUpdate) -> Trigger:
        try:
            await self.get_trigger(trigger_id, user_id)
            trigger_data = data.model_dump()
            trigger_data["updated_at"] = datetime.utcnow()
            trigger = await self.repository.update_one(trigger_data, id=trigger_id)
            await self.session.commit()
            return Trigger.model_validate(trigger)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barabashka"
            )

    async def delete_trigger(self, trigger_id: UUID4, user_id: UUID4) -> Trigger:
        await self.get_trigger(trigger_id, user_id)
        trigger = await self.repository.delete_one(id=trigger_id)
        await self.session.commit()
        return Trigger.model_validate(trigger)
