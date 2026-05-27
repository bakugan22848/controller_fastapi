from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.repositories.base_repository import BaseRepository
from app.repositories.controller_repository import ControllerRepository
from app.repositories.device_repository import DeviceRepository
from app.repositories.trigger_repository import TriggerRepository
from app.repositories.user_repository import UserRepository
from app.services.admin_service import AdminService
from app.services.controller_service import ControllerService

from app.services.device_service import DeviceService
from app.services.trigger_service import TriggerService
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.esp_service import EspService

session_dep = Annotated[AsyncSession, Depends(get_db)]

async def get_user_service(session: session_dep) -> UserService:
    user_repository = UserRepository(session)
    return UserService(session=session, repository=user_repository)

async def get_auth_service(session: session_dep) -> AuthService:
    user_repository = UserRepository(session)
    return AuthService(session=session, repository=user_repository)

async def get_device_service(session: session_dep) -> DeviceService:
    device_repository = DeviceRepository(session)
    trigger_repository = TriggerRepository(session)
    controller_repository = ControllerRepository(session)
    return DeviceService(session=session, repository=device_repository, trigger_repository=trigger_repository,
                         controller_repository=controller_repository)

async def get_trigger_service(session: session_dep) -> TriggerService:
    trigger_repository = TriggerRepository(session)
    device_repository = DeviceRepository(session)
    return TriggerService(session=session, repository=trigger_repository, device_repository=device_repository)

async def get_controller_service(session: session_dep) -> ControllerService:
    controller_repository = ControllerRepository(session)
    device_repository = DeviceRepository(session)
    return ControllerService(session=session, repository=controller_repository, device_repository=device_repository)

async def get_admin_service(session: session_dep) -> AdminService:
    base_repository = BaseRepository(session)
    return AdminService(session=session, repository=base_repository)

async def get_esp_service(session: session_dep) -> EspService:
    trigger_repository = TriggerRepository(session)
    controller_repository = ControllerRepository(session)
    device_repository = DeviceRepository(session)
    return EspService(
        session=session,
        trigger_repository=trigger_repository,
        controller_repository=controller_repository,
        device_repository=device_repository
    )

user_service_dep = Annotated[UserService, Depends(get_user_service)]
auth_service_dep = Annotated[AuthService, Depends(get_auth_service)]
device_service_dep = Annotated[DeviceService, Depends(get_device_service)]
trigger_service_dep = Annotated[TriggerService, Depends(get_trigger_service)]
controller_service_dep = Annotated[ControllerService, Depends(get_controller_service)]
admin_service_dep = Annotated[AdminService, Depends(get_admin_service)]
esp_service_dep = Annotated[EspService, Depends(get_esp_service)]








