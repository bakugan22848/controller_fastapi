from datetime import datetime

from typing import List

from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.controller_repository import ControllerRepository
from app.repositories.trigger_repository import TriggerRepository
from app.schemas.device_schemas import Device, DeviceCreate, DeviceUpdate, DeviceWCount
from app.repositories.device_repository import DeviceRepository

class DeviceService:
    def __init__(self, session: AsyncSession, repository: DeviceRepository, trigger_repository: TriggerRepository,
                 controller_repository: ControllerRepository):
        self.session = session
        self.repository = repository
        self.trigger_repository = trigger_repository
        self.controller_repository = controller_repository


    async def create_device(self, data: DeviceCreate, user_id:UUID4) -> Device:
        try:
            device_data = {
                "name": data.name,
                "user_id": user_id,
            }
            device = await self.repository.create_one(device_data)
            return Device.model_validate(device)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't connect device"
            )

    async def get_devices_by(self, user_id: UUID4) -> List[DeviceWCount]:
        devices = await self.repository.get_many_by(user_id=user_id)
        result = []
        for device in devices:
            count = await self.get_periph_count(device.id, user_id)
            result.append(DeviceWCount(
                id=device.id,
                name=device.name,
                user_id=device.user_id,
                periph_count=count,
                created_at=device.created_at,
                updated_at=device.updated_at
            ))
        return result

    async def get_periph_count(self, device_id:UUID4, user_id: UUID4) -> int:
        device = await self.repository.get_one(id=device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        if device.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        triggers = await self.trigger_repository.get_many_by(device_id=device_id)
        controllers = await self.controller_repository.get_many_by(device_id=device_id)
        triggers_count = len(triggers)
        controllers_count = len(controllers)
        count = triggers_count + controllers_count
        return count

    async def get_device(self, device_id: UUID4, user_id: UUID4) -> Device:
        device = await self.repository.get_one(id=device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        if device.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return Device.model_validate(device)

    async def update_device(self, device_id: UUID4, user_id: UUID4, data: DeviceUpdate) -> Device:
        try:
            await self.get_device(device_id, user_id)
            device_data = data.model_dump(exclude_none=True)

            device_data["updated_at"] = datetime.utcnow()

            device = await self.repository.update_one(device_data, id=device_id)
            await self.session.commit()
            return Device.model_validate(device)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't update device"
            )


    async def delete_device(self, device_id: UUID4, user_id: UUID4) -> Device:
        await self.get_device(device_id, user_id)
        device = await self.repository.delete_one(id=device_id)
        await self.session.commit()
        return Device.model_validate(device)
