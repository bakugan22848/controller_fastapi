from datetime import datetime
from pydantic import UUID4
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.trigger_repository import TriggerRepository
from app.repositories.controller_repository import ControllerRepository
from app.repositories.device_repository import DeviceRepository
from app.schemas.esp_schemas import TriggerValueOut, ControllerStateOut, TriggerValueIn
from app.schemas.trigger_schemas import Trigger


class EspService:
    def __init__(self, session: AsyncSession,
                 trigger_repository: TriggerRepository,
                 controller_repository: ControllerRepository,
                 device_repository: DeviceRepository):
        self.session = session
        self.trigger_repository = trigger_repository
        self.controller_repository = controller_repository
        self.device_repository = device_repository



    async def update_last_val(self, trigger_id: UUID4, payload: TriggerValueIn) -> TriggerValueIn:
        try:
            trigger = await self.trigger_repository.get_one(id=trigger_id)
            trigger.last_value = payload.value
            await self.triggering(trigger)
            await self.session.commit()
            return TriggerValueIn.model_validate(payload)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barabashka"
            )

    async def triggering(self, trigger: Trigger):
        controllers = await self.controller_repository.get_many_by(trigger_id=trigger.id)

        for controller in controllers:
            should_be_on = False

            if controller.trigger_vector is None:
                continue

            if controller.trigger_vector == "less":
                if trigger.last_value < controller.trigger_value:
                    should_be_on = True

            elif controller.trigger_vector == "more":
                if trigger.last_value > controller.trigger_value:
                    should_be_on = True

            if controller.last_state != should_be_on:
                controller.last_state = should_be_on
                controller.updated_at = datetime.utcnow()




    async def get_controller_state(self, controller_id: UUID4) -> ControllerStateOut:
        controller = await self.controller_repository.get_one(id=controller_id)
        if not controller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Controller not found"
            )

        return ControllerStateOut(
            controller_id=controller.id,
            last_state=controller.last_state,
        )

    async def ping_device(self, device_id: UUID4) -> dict:
        device = await self.device_repository.get_one(id=device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        now = datetime.utcnow()
        await self.device_repository.update_one(
            {"last_seen": now},
            id=device_id
        )
        await self.session.commit()

        return {"device_id": str(device_id), "last_seen": str(now)}