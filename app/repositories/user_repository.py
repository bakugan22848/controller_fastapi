from app.models.user_model import User
from app.schemas.user_schemas import User as UserSchema

from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model: UserSchema = User