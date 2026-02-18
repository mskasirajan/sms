from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.teacher_schema import (
    TeacherCreate, TeacherUpdate, TeacherResponse,
    StaffCreate, StaffResponse,
)
from app.services import teacher_service
from app.models.user import User

router = APIRouter()


@router.get("", response_model=dict)
def list_teachers(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return teacher_service.get_teachers(db, current_user.school_id, page, size, is_active)


@router.post("", response_model=TeacherResponse, status_code=201)
def create_teacher(
    payload: TeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Principal")),
):
    return teacher_service.create_teacher(db, current_user.school_id, payload)


@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return teacher_service.get_teacher(db, current_user.school_id, teacher_id)


@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: int,
    payload: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Principal")),
):
    return teacher_service.update_teacher(db, current_user.school_id, teacher_id, payload)


@router.delete("/{teacher_id}", status_code=204)
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin")),
):
    teacher_service.delete_teacher(db, current_user.school_id, teacher_id)


# --- Staff ---

@router.get("/staff/list", response_model=dict)
def list_staff(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return teacher_service.get_staff(db, current_user.school_id, page, size)


@router.post("/staff", response_model=StaffResponse, status_code=201)
def create_staff(
    payload: StaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin")),
):
    return teacher_service.create_staff(db, current_user.school_id, payload)
