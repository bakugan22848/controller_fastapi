from tokenize import TokenInfo
from uuid import UUID

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

import app.utils.auth_utils as auth
from app.database.database import get_db
from app.schemas.auth_schemas import TokenInfo

from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import SignUp, SignIn, User

security = HTTPBearer()

class AuthService:
    def __init__(self, session: AsyncSession, repository: UserRepository):
        self.session = session
        self.repository = repository

    async def sign_in(self, data: SignIn) -> TokenInfo:
        email = data.email
        password = data.password
        db_user = await self.repository.get_one(email=email)

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")


        if not auth.verify_password(plain_password=password, hashed_password=db_user.hashed_password):
            raise HTTPException(status_code=403, detail="Incorrect password")

        token = await auth.encode_jwt({"sub": str(db_user.id), "email": email})
        token_info = TokenInfo(access_token=token, token_type="Bearer")
        return token_info

    async def sign_up(self, data: SignUp) -> TokenInfo:
        email = data.email
        existing_email = await self.repository.get_one(email=email)
        if existing_email:
            raise HTTPException(status_code=404, detail="Email already registered")

        username = data.username
        existing_username = await self.repository.get_one(username=username)
        if existing_username:
            raise HTTPException(status_code=404, detail="Username already registered")

        password = data.password
        hashed_password = auth.hash_password(password=password)

        user_data = {
            'email': email,
            'username': username,
            "hashed_password" : hashed_password.decode('utf-8'),
        }

        new_user = await self.repository.create_one(user_data)

        token = await auth.encode_jwt({"sub": str(new_user.id), "email": email})
        token_info = TokenInfo(access_token=token, token_type="Bearer")
        return token_info

    @staticmethod
    async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security),
                               session: AsyncSession = Depends(get_db)) -> User:

        payload = auth.decode_jwt(token.credentials)

        if not payload:
            raise HTTPException(status_code=403, detail="Invalid credentials")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")

        user_repository = UserRepository(session=session)
        result = await user_repository.get_one(id=UUID(user_id))
        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        return result



