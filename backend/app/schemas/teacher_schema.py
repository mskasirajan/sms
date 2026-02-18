from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class TeacherCreate(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = 0
    joining_date: Optional[date] = None


class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    is_active: Optional[bool] = None


class TeacherResponse(BaseModel):
    id: int
    school_id: int
    employee_id: str
    first_name: str
    last_name: str
    phone: Optional[str]
    email: Optional[str]
    qualification: Optional[str]
    experience_years: int
    joining_date: Optional[date]
    is_active: bool

    model_config = {"from_attributes": True}


class StaffCreate(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    joining_date: Optional[date] = None


class StaffResponse(BaseModel):
    id: int
    school_id: int
    employee_id: str
    first_name: str
    last_name: str
    phone: Optional[str]
    email: Optional[str]
    role: Optional[str]
    department: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}
