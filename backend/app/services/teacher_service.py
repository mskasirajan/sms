from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.teacher import Teacher, Staff
from app.schemas.teacher_schema import TeacherCreate, TeacherUpdate, StaffCreate
from typing import Optional


def get_teachers(db: Session, school_id: int, page: int = 1, size: int = 20,
                 is_active: Optional[bool] = None):
    query = db.query(Teacher).filter(Teacher.school_id == school_id)
    if is_active is not None:
        query = query.filter(Teacher.is_active == is_active)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}


def get_teacher(db: Session, school_id: int, teacher_id: int) -> Teacher:
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id, Teacher.school_id == school_id
    ).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


def create_teacher(db: Session, school_id: int, payload: TeacherCreate) -> Teacher:
    existing = db.query(Teacher).filter(
        Teacher.school_id == school_id,
        Teacher.employee_id == payload.employee_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee ID already exists")

    teacher = Teacher(school_id=school_id, **payload.model_dump())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def update_teacher(db: Session, school_id: int, teacher_id: int, payload: TeacherUpdate) -> Teacher:
    teacher = get_teacher(db, school_id, teacher_id)
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(teacher, field, value)
    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, school_id: int, teacher_id: int):
    teacher = get_teacher(db, school_id, teacher_id)
    db.delete(teacher)
    db.commit()


def get_staff(db: Session, school_id: int, page: int = 1, size: int = 20):
    query = db.query(Staff).filter(Staff.school_id == school_id)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}


def create_staff(db: Session, school_id: int, payload: StaffCreate) -> Staff:
    staff = Staff(school_id=school_id, **payload.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff
