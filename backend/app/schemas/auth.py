from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str
    institution_id: Optional[int] = None
    kitchen_id: Optional[int] = None
    processing_unit_id: Optional[int] = None
    ngo_id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    institution_id: Optional[int] = None
    kitchen_id: Optional[int] = None
    processing_unit_id: Optional[int] = None
    ngo_id: Optional[int] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
