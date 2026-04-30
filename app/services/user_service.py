from datetime import datetime

from argon2 import PasswordHasher
from typing import List

from argon2.exceptions import VerifyMismatchError
from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import User, SignUp,  UserDetails, UserUpdate, UserList
from app.repositories.user_repository import UserRepository


ph = PasswordHasher()

class UserService:
    def __init__(self, session: AsyncSession, repository: UserRepository):
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
            await self.session.commit()
            return User.model_validate(user)


        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists"
            )

    async def get_users(self) -> List[User]:
        users = await self.repository.get_many()
        return users

    async def get_user(self, user_id: UUID4) -> User:
        user = await self.repository.get_one(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return User.model_validate(user)

    async def update_user(self, user_id: UUID4, data: UserUpdate) -> User:
        try:
            user_exist = await self.get_user(user_id)
            user_data = data.model_dump()

            try:
                if ph.verify(
                        user_exist.hashed_password.encode("utf-8"),
                        user_data["password"]
                ):
                    del user_data["password"]
            except VerifyMismatchError:
                user_data['hashed_password'] = ph.hash(user_data.pop('password').encode('utf-8'))

            user_data["updated_at"] = datetime.utcnow()

            user = await self.repository.update_one(user_data, id=user_id)
            await self.session.commit()
            return User.model_validate(user)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists"
            )


    async def delete_user(self, user_id: UUID4) -> User:
        await self.get_user(user_id)
        user = await self.repository.delete_one(id=user_id)
        await self.session.commit()
        return User.model_validate(user)
