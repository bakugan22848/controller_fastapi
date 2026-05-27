from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, UUID4

class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class User(TunedModel):
    id: UUID4
    email: EmailStr = Field(max_length=50)
    username: str = Field(max_length=50)
    hashed_password: str = Field(max_length=350)
    created_at: datetime
    updated_at: datetime

class SignUp(BaseModel):
    email: EmailStr = Field(max_length=50)
    username: str = Field(max_length=50)
    password: str = Field(max_length=50)

class SignIn(BaseModel):
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=50)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(max_length=50)
    username: Optional[str] = Field(max_length=50)
    password: Optional[str] = Field(max_length=50)

class UserList(TunedModel):
    users: List[User]

class UserDetails(TunedModel):
    user: User