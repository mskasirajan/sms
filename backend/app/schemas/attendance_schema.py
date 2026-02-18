from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date
from app.models.attendance import AttendanceStatus


class AttendanceRecord(BaseModel):
    student_id: int
    status: AttendanceStatus
    remarks: Optional[str] = None


class MarkAttendanceRequest(BaseModel):
    class_id: int
    section_id: Optional[int] = None
    teacher_id: int
    date: date
    period: int = 1
    records: List[AttendanceRecord]


class AttendanceSessionResponse(BaseModel):
    id: int
    school_id: int
    class_id: int
    section_id: Optional[int]
    teacher_id: int
    date: date
    period: int

    model_config = {"from_attributes": True}


class StudentAttendanceResponse(BaseModel):
    id: int
    session_id: int
    student_id: int
    status: str
    remarks: Optional[str]

    model_config = {"from_attributes": True}


class AttendanceReportRequest(BaseModel):
    class_id: int
    section_id: Optional[int] = None
    start_date: date
    end_date: date


class StudentAttendanceSummary(BaseModel):
    student_id: int
    student_name: str
    total_days: int
    present: int
    absent: int
    late: int
    half_day: int
    attendance_percentage: float
