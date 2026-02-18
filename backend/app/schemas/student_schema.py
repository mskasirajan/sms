from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from app.models.student import GenderEnum, StudentStatus


class ParentCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: Optional[EmailStr] = None
    occupation: Optional[str] = None
    relation: Optional[str] = None  # Father, Mother, Guardian


class ParentResponse(BaseModel):
    id: int
    school_id: int
    first_name: str
    last_name: str
    phone: str
    email: Optional[str]
    occupation: Optional[str]
    relation: Optional[str]

    model_config = {"from_attributes": True}


class StudentCreate(BaseModel):
    admission_no: str
    first_name: str
    last_name: str
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    address: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    academic_year_id: Optional[int] = None
    parent_ids: Optional[List[int]] = []


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    address: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    status: Optional[StudentStatus] = None


class StudentResponse(BaseModel):
    id: int
    school_id: int
    admission_no: str
    first_name: str
    last_name: str
    dob: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    class_id: Optional[int]
    section_id: Optional[int]
    academic_year_id: Optional[int]
    status: str

    model_config = {"from_attributes": True}


class StudentListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[StudentResponse]
