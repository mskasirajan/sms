from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text, Numeric, Enum, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import enum
from app.core.database import Base


class ExamType(str, enum.Enum):
    unit_test = "Unit Test"
    midterm = "Midterm"
    final = "Final"
    quarterly = "Quarterly"
    half_yearly = "Half Yearly"
    annual = "Annual"


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    name = Column(String(255), nullable=False)
    exam_type = Column(Enum(ExamType), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    schedule = relationship("ExamSchedule", back_populates="exam")
    marks = relationship("Mark", back_populates="exam")
    report_cards = relationship("ReportCard", back_populates="exam")


class ExamSchedule(Base):
    __tablename__ = "exam_schedule"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    max_marks = Column(Numeric(6, 2), nullable=False)
    passing_marks = Column(Numeric(6, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    exam = relationship("Exam", back_populates="schedule")


class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    marks_obtained = Column(Numeric(6, 2))
    max_marks = Column(Numeric(6, 2))
    grade = Column(String(5))
    is_absent = Column(Boolean, default=False)
    remarks = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    exam = relationship("Exam", back_populates="marks")
    student = relationship("Student", back_populates="marks")


class ReportCard(Base):
    __tablename__ = "report_cards"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    total_marks_obtained = Column(Numeric(8, 2))
    total_max_marks = Column(Numeric(8, 2))
    percentage = Column(Numeric(5, 2))
    grade = Column(String(5))
    rank = Column(Integer)
    remarks = Column(Text)
    is_published = Column(Boolean, default=False)
    pdf_url = Column(String(512))
    created_at = Column(DateTime, server_default=func.now())

    exam = relationship("Exam", back_populates="report_cards")
    student = relationship("Student")
