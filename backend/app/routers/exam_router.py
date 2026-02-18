from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.exam_schema import (
    ExamCreate, ExamResponse,
    UploadMarksRequest, MarkResponse,
    ReportCardResponse,
)
from app.services import exam_service
from app.models.user import User

router = APIRouter()


@router.post("/create", response_model=ExamResponse, status_code=201)
def create_exam(
    payload: ExamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Principal")),
):
    return exam_service.create_exam(db, current_user.school_id, payload)


@router.get("", response_model=List[ExamResponse])
def list_exams(
    academic_year_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return exam_service.get_exams(db, current_user.school_id, academic_year_id)


@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return exam_service.get_exam(db, current_user.school_id, exam_id)


@router.post("/marks/upload", response_model=List[MarkResponse], status_code=201)
def upload_marks(
    payload: UploadMarksRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Teacher", "School Admin")),
):
    return exam_service.upload_marks(db, current_user.school_id, payload)


@router.post("/{exam_id}/reportcards/generate", response_model=List[ReportCardResponse])
def generate_report_cards(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Principal")),
):
    return exam_service.generate_report_cards(db, current_user.school_id, exam_id)


@router.get("/reportcard/{exam_id}/{student_id}", response_model=ReportCardResponse)
def get_report_card(
    exam_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return exam_service.get_report_card(db, current_user.school_id, exam_id, student_id)
