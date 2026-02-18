from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.attendance_schema import (
    MarkAttendanceRequest, AttendanceSessionResponse,
    StudentAttendanceResponse, AttendanceReportRequest, StudentAttendanceSummary,
)
from app.services import attendance_service
from app.models.user import User

router = APIRouter()


@router.post("/session", response_model=AttendanceSessionResponse, status_code=201)
def mark_attendance(
    payload: MarkAttendanceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Teacher", "School Admin")),
):
    return attendance_service.mark_attendance(db, current_user.school_id, payload)


@router.get("/session/{session_id}", response_model=List[StudentAttendanceResponse])
def get_session_records(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return attendance_service.get_session_records(db, current_user.school_id, session_id)


@router.post("/report", response_model=List[StudentAttendanceSummary])
def attendance_report(
    payload: AttendanceReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return attendance_service.get_attendance_report(db, current_user.school_id, payload)
