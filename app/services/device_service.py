from datetime import datetime

from typing import List

from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.device_schemas import Device, DeviceCreate, DeviceUpdate
from app.repositories.device_repository import DeviceRepository


class DeviceService:
    def __init__(self, session: AsyncSession, repository: DeviceRepository):
        self.session = session
        self.repository = repository


    async def create_device(self, data: DeviceCreate) -> Device:
        try:
            name = data.name
            user_id = data.user_id

            device_data = {
                "name": name,
                "user_id": user_id,
            }

            device = await self.repository.create_one(device_data)
            await self.session.commit()
            return Device.model_validate(device)


        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't connect device"
            )

    async def get_devices(self) -> List[Device]:
        devices = await self.repository.get_many()
        return devices

    async def get_devices_by(self, user_id: UUID4) -> List[Device]:
        devices = await self.repository.get_many_by(user_id=user_id)
        return devices

    async def get_device(self, device_id: UUID4) -> Device:
        device = await self.repository.get_one(id=device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        return Device.model_validate(device)

    async def update_device(self, device_id: UUID4, data: DeviceUpdate) -> Device:
        try:
            device_exist = await self.get_device(device_id)
            device_data = data.model_dump()

            device_data["updated_at"] = datetime.utcnow()

            device = await self.repository.update_one(device_data, id=device_id)
            await self.session.commit()
            return Device.model_validate(device)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barabashka"
            )


    async def delete_device(self, device_id: UUID4) -> Device:
        await self.get_device(device_id)
        device = await self.repository.delete_one(id=device_id)
        await self.session.commit()
        return Device.model_validate(device)
