from datetime import datetime

from pydantic import UUID4

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import User, UserUpdate
from app.repositories.user_repository import UserRepository
import app.utils.auth_utils as auth



class UserService:
    def __init__(self, session: AsyncSession, repository: UserRepository):
        self.session = session
        self.repository = repository

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
            user_data = data.model_dump(exclude_none=True)

            if "password" in user_data:
                if auth.verify_password(user_data["password"], user_exist.hashed_password):
                    del user_data["password"]
                else:
                    user_data['hashed_password'] = auth.hash_password(user_data.pop('password')).decode('utf-8')

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
