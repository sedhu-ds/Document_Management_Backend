from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Only during creation

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes  = True

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes  = True
