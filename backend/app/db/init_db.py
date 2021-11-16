from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.core.config import get_settings
from app.services.user import UsersService
from app.schemas.user import UserCreate

settings = get_settings()


def init_db(db: Session):
    Base.metadata.create_all(bind=engine)
    users = UsersService(db)
    user = users.get_by_email(settings.SUPERUSER_EMAIL)
    if not user:
        create = UserCreate(
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD,
            full_name=settings.SUPERUSER_NAME,
            is_superuser=True,
        )
        users.create(create)
