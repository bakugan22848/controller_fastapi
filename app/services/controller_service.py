from datetime import datetime

from typing import List

from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.device_repository import DeviceRepository
from app.schemas.controller_schemas import Controller, ControllerCreate, ControllerUpdate
from app.repositories.controller_repository import ControllerRepository


class ControllerService:
    def __init__(self, session: AsyncSession, repository: ControllerRepository, device_repository: DeviceRepository):
        self.session = session
        self.repository = repository
        self.device_repository = device_repository


    async def create_controller(self, data: ControllerCreate, user_id: UUID4) -> Controller:
        try:
            device = await self.device_repository.get_one(id=data.device_id)
            if not device:
                raise HTTPException(status_code=404, detail="Device not found")
            if device.user_id != user_id:
                raise HTTPException(status_code=403, detail="Access denied")

            controller_data = {
                "name": data.name,
                "device_id": data.device_id,
                "trigger_value": data.trigger_value,
            }

            controller = await self.repository.create_one(controller_data)
            await self.session.commit()
            return Controller.model_validate(controller)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't connect trigger"
            )


    async def get_controllers_by(self, device_id: UUID4, user_id: UUID4) -> List[Controller]:
        device = await self.device_repository.get_one(id=device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        if device.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        controllers = await self.repository.get_many_by(device_id=device_id)
        return controllers

    async def get_controller(self, controller_id: UUID4, user_id: UUID4) -> Controller:
        controller = await self.repository.get_one(id=controller_id)
        if not controller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found")
        device = await self.device_repository.get_one(id=controller.device_id)
        if device.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        return Controller.model_validate(controller)

    async def update_controller(self, controller_id: UUID4, user_id: UUID4, data: ControllerUpdate) -> Controller:
        try:
            await self.get_controller(controller_id, user_id)
            controller_data = data.model_dump(exclude_none=True)

            controller_data["updated_at"] = datetime.utcnow()

            controller = await self.repository.update_one(controller_data, id=controller_id)
            await self.session.commit()
            return Controller.model_validate(controller)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't update controller"
            )


    async def delete_controller(self, controller_id: UUID4, user_id: UUID4) -> Controller:
        await self.get_controller(controller_id, user_id)
        controller = await self.repository.delete_one(id=controller_id)
        await self.session.commit()
        return Controller.model_validate(controller)
