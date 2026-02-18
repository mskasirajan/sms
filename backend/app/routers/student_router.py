from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.student_schema import (
    StudentCreate, StudentUpdate, StudentResponse, StudentListResponse,
    ParentCreate, ParentResponse,
)
from app.services import student_service
from app.models.user import User

router = APIRouter()


@router.get("", response_model=StudentListResponse)
def list_students(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return student_service.get_students(db, current_user.school_id, page, size, class_id, section_id)


@router.post("", response_model=StudentResponse, status_code=201)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Principal")),
):
    return student_service.create_student(db, current_user.school_id, payload)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return student_service.get_student(db, current_user.school_id, student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Principal")),
):
    return student_service.update_student(db, current_user.school_id, student_id, payload)


@router.delete("/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin")),
):
    student_service.delete_student(db, current_user.school_id, student_id)


# --- Parents ---

@router.post("/parents", response_model=ParentResponse, status_code=201)
def create_parent(
    payload: ParentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Principal")),
):
    return student_service.create_parent(db, current_user.school_id, payload)
