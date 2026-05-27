from typing import List
from argon2 import PasswordHasher

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.schemas.controller_schemas import Controller
from app.schemas.device_schemas import Device
from app.schemas.trigger_schemas import Trigger
from app.schemas.user_schemas import SignUp, User


ph = PasswordHasher()

class AdminService:
    def __init__(self, session: AsyncSession, repository: BaseRepository):
        self.session = session
        self.repository = repository

    async def create_user(self, data: SignUp) -> User:
        try:
            email = data.email
            username = data.username
            password = data.password

            hashed_password = ph.hash(password.encode('utf-8'))

            user_data = {
                "email": email,
                "username": username,
                "hashed_password": hashed_password,
            }

            user = await self.repository.create_one(user_data)
            return User.model_validate(user)


        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists"
            )

    async def get_users(self) -> List[User]:
        users = await self.repository.get_many()
        return users

    async def get_devices(self) -> List[Device]:
        devices = await self.repository.get_many()
        return devices

    async def get_triggers(self) -> List[Trigger]:
        triggers = await self.repository.get_many()
        return triggers

    async def get_controllers(self) -> List[Controller]:
        controllers = await self.repository.get_many()
        return controllers