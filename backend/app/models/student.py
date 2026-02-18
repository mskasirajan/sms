from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import enum
from app.core.database import Base


class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class StudentStatus(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"
    transferred = "Transferred"
    graduated = "Graduated"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admission_no = Column(String(50), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date)
    gender = Column(Enum(GenderEnum))
    address = Column(Text)
    photo_url = Column(String(512))
    class_id = Column(Integer, ForeignKey("classes.id"))
    section_id = Column(Integer, ForeignKey("sections.id"))
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"))
    status = Column(Enum(StudentStatus), default=StudentStatus.active)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="student_profile")
    class_ = relationship("Class")
    section = relationship("Section")
    academic_year = relationship("AcademicYear")
    parent_mappings = relationship("StudentParentMapping", back_populates="student")
    class_history = relationship("StudentClassHistory", back_populates="student")
    attendances = relationship("StudentAttendance", back_populates="student")
    marks = relationship("Mark", back_populates="student")
    invoices = relationship("Invoice", back_populates="student")


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255))
    occupation = Column(String(100))
    relation = Column(String(50))  # Father, Mother, Guardian
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="parent_profile")
    student_mappings = relationship("StudentParentMapping", back_populates="parent")


class StudentParentMapping(Base):
    __tablename__ = "student_parent_mapping"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    is_primary = Column(Boolean, default=False)

    student = relationship("Student", back_populates="parent_mappings")
    parent = relationship("Parent", back_populates="student_mappings")


class StudentClassHistory(Base):
    __tablename__ = "student_class_history"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"))
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="class_history")
