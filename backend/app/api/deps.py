from typing import Generator, Type

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core import security
from app.db.session import SessionLocal
from app.models import User
from app.services import UsersService
from app.services.base import BaseService
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/access-token")
settings = get_settings()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_service(service: Type[BaseService]):
    def get_depend_service(db: Session = Depends(get_db)):
        return service(db)

    return get_depend_service


def get_current_user(
    users: UsersService = Depends(get_service(UsersService)),
    token: str = Depends(reusable_oauth2),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    if user := users.get(token_data.sub):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User")


def get_current_active_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user
