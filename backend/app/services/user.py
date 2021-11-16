from typing import Union, Dict, Any, Optional
from sqlalchemy.orm import Session

from .base import BaseService
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserAuth


class UsersService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, create: UserCreate) -> User:
        obj = User(
            email=create.email,
            hashed_password=get_password_hash(create.password),
            full_name=create.full_name,
            is_active=create.is_active,
            is_superuser=create.is_superuser,
        )
        return self.commit(obj)

    def update(
        self,
        obj: User,
        update: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        update_data = self.get_update_data(update)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(obj, update)

    def authenticate(self, auth: UserAuth) -> Optional[User]:
        user = self.db.query(User).filter(User.email == auth.email).first()
        if not user or not verify_password(auth.password, user.hashed_password):
            return None
        return user
