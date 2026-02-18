from pydantic import BaseModel, EmailStr
from typing import Optional, List


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserCreate(BaseModel):
    school_id: int
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role_names: List[str] = []


class UserResponse(BaseModel):
    id: int
    school_id: int
    email: str
    phone: Optional[str]
    is_active: bool
    roles: List[str] = []

    model_config = {"from_attributes": True}


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
