from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None


class UserDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class User(UserDBBase):
    pass
