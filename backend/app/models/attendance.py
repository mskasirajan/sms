from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Enum, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import enum
from app.core.database import Base


class AttendanceStatus(str, enum.Enum):
    present = "Present"
    absent = "Absent"
    late = "Late"
    half_day = "Half-Day"


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    date = Column(Date, nullable=False)
    period = Column(Integer, default=1)  # 1 = full day, or period number
    created_at = Column(DateTime, server_default=func.now())

    teacher = relationship("Teacher", back_populates="attendance_sessions")
    student_records = relationship("StudentAttendance", back_populates="session")


class StudentAttendance(Base):
    __tablename__ = "student_attendance"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    remarks = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    session = relationship("AttendanceSession", back_populates="student_records")
    student = relationship("Student", back_populates="attendances")
