from datetime import datetime

from typing import List

from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.controller_schemas import Controller, ControllerCreate, ControllerUpdate
from app.repositories.controller_repository import ControllerRepository


class ControllerService:
    def __init__(self, session: AsyncSession, repository: ControllerRepository):
        self.session = session
        self.repository = repository


    async def create_controller(self, data: ControllerCreate) -> Controller:
        try:
            name = data.name
            device_id = data.device_id
            trigger_id = data.trigger_id


            controller_data = {
                "name": name,
                "device_id": device_id,
                "trigger_id": trigger_id,

            }

            controller = await self.repository.create_one(controller_data)
            await self.session.commit()
            return Controller.model_validate(controller)


        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't connect trigger"
            )

    async def get_controllers(self) -> List[Controller]:
        controllers = await self.repository.get_many()
        return controllers

    async def get_devices_by(self, device_id: UUID4) -> List[Controller]:
        controllers = await self.repository.get_many_by(device_id=device_id)
        return controllers

    async def get_controller(self, controller_id: UUID4) -> Controller:
        controller = await self.repository.get_one(id=controller_id)
        if not controller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        return Controller.model_validate(controller)

    async def update_controller(self, controller_id: UUID4, data: ControllerUpdate) -> Controller:
        try:
            controller_exist = await self.get_controller(controller_id)
            controller_data = data.model_dump()

            controller_data["updated_at"] = datetime.utcnow()

            controller = await self.repository.update_one(controller_data, id=controller_id)
            await self.session.commit()
            return Controller.model_validate(controller)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barabashka"
            )


    async def delete_controller(self, controller_id: UUID4) -> Controller:
        await self.get_controller(controller_id)
        controller = await self.repository.delete_one(id=controller_id)
        await self.session.commit()
        return Controller.model_validate(controller)
