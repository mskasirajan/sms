from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.attendance import AttendanceSession, StudentAttendance, AttendanceStatus
from app.models.student import Student
from app.schemas.attendance_schema import MarkAttendanceRequest, AttendanceReportRequest
from datetime import date


def mark_attendance(db: Session, school_id: int, payload: MarkAttendanceRequest):
    # Prevent duplicate session for same class/date/period
    existing = db.query(AttendanceSession).filter(
        AttendanceSession.school_id == school_id,
        AttendanceSession.class_id == payload.class_id,
        AttendanceSession.section_id == payload.section_id,
        AttendanceSession.date == payload.date,
        AttendanceSession.period == payload.period,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance already marked for this class/date/period"
        )

    session = AttendanceSession(
        school_id=school_id,
        class_id=payload.class_id,
        section_id=payload.section_id,
        teacher_id=payload.teacher_id,
        date=payload.date,
        period=payload.period,
    )
    db.add(session)
    db.flush()

    for record in payload.records:
        entry = StudentAttendance(
            school_id=school_id,
            session_id=session.id,
            student_id=record.student_id,
            status=record.status,
            remarks=record.remarks,
        )
        db.add(entry)

    db.commit()
    db.refresh(session)
    return session


def get_session_records(db: Session, school_id: int, session_id: int):
    session = db.query(AttendanceSession).filter(
        AttendanceSession.id == session_id,
        AttendanceSession.school_id == school_id
    ).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return session.student_records


def get_attendance_report(db: Session, school_id: int, payload: AttendanceReportRequest):
    sessions = db.query(AttendanceSession).filter(
        AttendanceSession.school_id == school_id,
        AttendanceSession.class_id == payload.class_id,
        AttendanceSession.date >= payload.start_date,
        AttendanceSession.date <= payload.end_date,
    )
    if payload.section_id:
        sessions = sessions.filter(AttendanceSession.section_id == payload.section_id)

    session_ids = [s.id for s in sessions.all()]
    if not session_ids:
        return []

    # Get all students in the class
    student_query = db.query(Student).filter(
        Student.school_id == school_id,
        Student.class_id == payload.class_id,
    )
    if payload.section_id:
        student_query = student_query.filter(Student.section_id == payload.section_id)
    students = student_query.all()

    total_days = len(session_ids)
    report = []
    for student in students:
        records = db.query(StudentAttendance).filter(
            StudentAttendance.session_id.in_(session_ids),
            StudentAttendance.student_id == student.id,
        ).all()
        counts = {s: 0 for s in AttendanceStatus}
        for r in records:
            counts[r.status] += 1

        present = counts[AttendanceStatus.present]
        late = counts[AttendanceStatus.late]
        half_day = counts[AttendanceStatus.half_day]
        absent = counts[AttendanceStatus.absent]
        effective_present = present + late + (half_day * 0.5)
        pct = round((effective_present / total_days * 100), 2) if total_days else 0.0

        report.append({
            "student_id": student.id,
            "student_name": f"{student.first_name} {student.last_name}",
            "total_days": total_days,
            "present": present,
            "absent": absent,
            "late": late,
            "half_day": half_day,
            "attendance_percentage": pct,
        })

    return report
