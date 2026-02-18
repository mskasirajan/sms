from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.student import Student, Parent, StudentParentMapping, StudentClassHistory
from app.schemas.student_schema import StudentCreate, StudentUpdate
from typing import Optional


def get_students(db: Session, school_id: int, page: int = 1, size: int = 20,
                 class_id: Optional[int] = None, section_id: Optional[int] = None):
    query = db.query(Student).filter(Student.school_id == school_id)
    if class_id:
        query = query.filter(Student.class_id == class_id)
    if section_id:
        query = query.filter(Student.section_id == section_id)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}


def get_student(db: Session, school_id: int, student_id: int) -> Student:
    student = db.query(Student).filter(
        Student.id == student_id, Student.school_id == school_id
    ).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


def create_student(db: Session, school_id: int, payload: StudentCreate) -> Student:
    existing = db.query(Student).filter(
        Student.school_id == school_id,
        Student.admission_no == payload.admission_no
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admission number already exists")

    student = Student(
        school_id=school_id,
        admission_no=payload.admission_no,
        first_name=payload.first_name,
        last_name=payload.last_name,
        dob=payload.dob,
        gender=payload.gender,
        address=payload.address,
        class_id=payload.class_id,
        section_id=payload.section_id,
        academic_year_id=payload.academic_year_id,
    )
    db.add(student)
    db.flush()

    # Link parents
    for parent_id in (payload.parent_ids or []):
        parent = db.query(Parent).filter(Parent.id == parent_id, Parent.school_id == school_id).first()
        if parent:
            mapping = StudentParentMapping(student_id=student.id, parent_id=parent.id)
            db.add(mapping)

    # Record class history
    if payload.class_id and payload.academic_year_id:
        history = StudentClassHistory(
            school_id=school_id,
            student_id=student.id,
            class_id=payload.class_id,
            section_id=payload.section_id,
            academic_year_id=payload.academic_year_id,
        )
        db.add(history)

    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, school_id: int, student_id: int, payload: StudentUpdate) -> Student:
    student = get_student(db, school_id, student_id)
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, school_id: int, student_id: int):
    student = get_student(db, school_id, student_id)
    db.delete(student)
    db.commit()


def create_parent(db: Session, school_id: int, payload) -> Parent:
    parent = Parent(school_id=school_id, **payload.model_dump())
    db.add(parent)
    db.commit()
    db.refresh(parent)
    return parent
