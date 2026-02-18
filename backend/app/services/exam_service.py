from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.exam import Exam, ExamSchedule, Mark, ReportCard
from app.models.student import Student
from app.schemas.exam_schema import ExamCreate, UploadMarksRequest
from decimal import Decimal


GRADE_SCALE = [
    (90, "A+"), (80, "A"), (70, "B+"), (60, "B"),
    (50, "C"), (40, "D"), (0, "F"),
]


def _compute_grade(percentage: float) -> str:
    for threshold, grade in GRADE_SCALE:
        if percentage >= threshold:
            return grade
    return "F"


def create_exam(db: Session, school_id: int, payload: ExamCreate) -> Exam:
    exam = Exam(
        school_id=school_id,
        academic_year_id=payload.academic_year_id,
        name=payload.name,
        exam_type=payload.exam_type,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
    db.add(exam)
    db.flush()

    for sched in payload.schedule:
        entry = ExamSchedule(exam_id=exam.id, **sched.model_dump())
        db.add(entry)

    db.commit()
    db.refresh(exam)
    return exam


def get_exams(db: Session, school_id: int, academic_year_id: int = None):
    query = db.query(Exam).filter(Exam.school_id == school_id)
    if academic_year_id:
        query = query.filter(Exam.academic_year_id == academic_year_id)
    return query.all()


def get_exam(db: Session, school_id: int, exam_id: int) -> Exam:
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.school_id == school_id).first()
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return exam


def upload_marks(db: Session, school_id: int, payload: UploadMarksRequest):
    exam = get_exam(db, school_id, payload.exam_id)

    # Get max_marks per subject from exam schedule
    schedule_map = {s.subject_id: s.max_marks for s in exam.schedule}

    created = []
    for entry in payload.entries:
        # Upsert: remove existing mark if any
        existing = db.query(Mark).filter(
            Mark.exam_id == exam.id,
            Mark.student_id == entry.student_id,
            Mark.subject_id == entry.subject_id,
        ).first()
        if existing:
            db.delete(existing)
            db.flush()

        max_marks = schedule_map.get(entry.subject_id)
        grade = None
        if not entry.is_absent and entry.marks_obtained is not None and max_marks:
            pct = float(entry.marks_obtained) / float(max_marks) * 100
            grade = _compute_grade(pct)

        mark = Mark(
            school_id=school_id,
            exam_id=exam.id,
            student_id=entry.student_id,
            subject_id=entry.subject_id,
            marks_obtained=entry.marks_obtained,
            max_marks=max_marks,
            grade=grade,
            is_absent=entry.is_absent,
            remarks=entry.remarks,
        )
        db.add(mark)
        created.append(mark)

    db.commit()
    return created


def generate_report_cards(db: Session, school_id: int, exam_id: int):
    exam = get_exam(db, school_id, exam_id)

    # Find all students who have marks for this exam
    student_ids = db.query(Mark.student_id).filter(
        Mark.exam_id == exam_id, Mark.school_id == school_id
    ).distinct().all()
    student_ids = [s[0] for s in student_ids]

    report_cards = []
    percentages = {}

    for sid in student_ids:
        marks = db.query(Mark).filter(
            Mark.exam_id == exam_id, Mark.student_id == sid
        ).all()

        total_obtained = sum(
            m.marks_obtained for m in marks if not m.is_absent and m.marks_obtained is not None
        )
        total_max = sum(
            m.max_marks for m in marks if m.max_marks is not None
        )
        pct = round(float(total_obtained) / float(total_max) * 100, 2) if total_max else 0.0
        grade = _compute_grade(pct)
        percentages[sid] = pct

        # Remove existing report card
        db.query(ReportCard).filter(
            ReportCard.exam_id == exam_id, ReportCard.student_id == sid
        ).delete()

        rc = ReportCard(
            school_id=school_id,
            exam_id=exam_id,
            student_id=sid,
            total_marks_obtained=total_obtained,
            total_max_marks=total_max,
            percentage=pct,
            grade=grade,
        )
        db.add(rc)
        report_cards.append(rc)

    db.flush()

    # Calculate ranks by percentage descending
    sorted_ids = sorted(percentages, key=lambda k: percentages[k], reverse=True)
    for rank, sid in enumerate(sorted_ids, start=1):
        rc = next(r for r in report_cards if r.student_id == sid)
        rc.rank = rank

    db.commit()
    return report_cards


def get_report_card(db: Session, school_id: int, exam_id: int, student_id: int) -> ReportCard:
    rc = db.query(ReportCard).filter(
        ReportCard.exam_id == exam_id,
        ReportCard.student_id == student_id,
        ReportCard.school_id == school_id,
    ).first()
    if not rc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report card not found")
    return rc
