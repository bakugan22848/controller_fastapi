from datetime import datetime

from typing import List

from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.trigger_schemas import Trigger, TriggerCreate, TriggerUpdate
from app.repositories.trigger_repository import TriggerRepository


class TriggerService:
    def __init__(self, session: AsyncSession, repository: TriggerRepository):
        self.session = session
        self.repository = repository


    async def create_trigger(self, data: TriggerCreate) -> Trigger:
        try:
            name = data.name
            device_id = data.device_id
            controller_id = data.controller_id
            notif_value = data.notif_value
            check_clock = data.check_clock
            write_clock = data.write_clock

            trigger_data = {
                "name": name,
                "device_id": device_id,
                "controller_id": controller_id,
                "notif_value": notif_value,
                "check_clock": check_clock,
                "write_clock": write_clock
            }

            trigger = await self.repository.create_one(trigger_data)
            await self.session.commit()
            return Trigger.model_validate(trigger)


        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't connect trigger"
            )

    async def get_triggers(self) -> List[Trigger]:
        triggers = await self.repository.get_many()
        return triggers

    async def get_triggers_by(self, device_id: UUID4) -> List[Trigger]:
        triggers = await self.repository.get_many_by(device_id=device_id)
        return triggers

    async def get_trigger(self, trigger_id: UUID4) -> Trigger:
        trigger = await self.repository.get_one(id=trigger_id)
        if not trigger:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        return Trigger.model_validate(trigger)

    async def update_trigger(self, trigger_id: UUID4, data: TriggerUpdate) -> Trigger:
        try:
            trigger_exist = await self.get_trigger(trigger_id)
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


    async def delete_trigger(self, trigger_id: UUID4) -> Trigger:
        await self.get_trigger(trigger_id)
        trigger = await self.repository.delete_one(id=trigger_id)
        await self.session.commit()
        return Trigger.model_validate(trigger)
