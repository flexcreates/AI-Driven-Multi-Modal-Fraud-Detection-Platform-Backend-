from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: str # Required by schema
    is_active: Optional[bool] = True
    role: Optional[str] = "USER"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: UUID
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
