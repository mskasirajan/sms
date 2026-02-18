from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time
from decimal import Decimal
from app.models.exam import ExamType


class ExamScheduleCreate(BaseModel):
    subject_id: int
    class_id: int
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    max_marks: Decimal
    passing_marks: Decimal


class ExamCreate(BaseModel):
    academic_year_id: int
    name: str
    exam_type: ExamType
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    schedule: List[ExamScheduleCreate] = []


class ExamResponse(BaseModel):
    id: int
    school_id: int
    academic_year_id: int
    name: str
    exam_type: str
    start_date: Optional[date]
    end_date: Optional[date]
    is_published: bool

    model_config = {"from_attributes": True}


class MarkEntry(BaseModel):
    student_id: int
    subject_id: int
    marks_obtained: Optional[Decimal] = None
    is_absent: bool = False
    remarks: Optional[str] = None


class UploadMarksRequest(BaseModel):
    exam_id: int
    entries: List[MarkEntry]


class MarkResponse(BaseModel):
    id: int
    exam_id: int
    student_id: int
    subject_id: int
    marks_obtained: Optional[Decimal]
    max_marks: Optional[Decimal]
    grade: Optional[str]
    is_absent: bool

    model_config = {"from_attributes": True}


class ReportCardResponse(BaseModel):
    id: int
    exam_id: int
    student_id: int
    total_marks_obtained: Optional[Decimal]
    total_max_marks: Optional[Decimal]
    percentage: Optional[Decimal]
    grade: Optional[str]
    rank: Optional[int]
    remarks: Optional[str]
    is_published: bool
    pdf_url: Optional[str]

    model_config = {"from_attributes": True}
