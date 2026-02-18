from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import enum
from app.core.database import Base


class InvoiceStatus(str, enum.Enum):
    pending = "Pending"
    partial = "Partial"
    paid = "Paid"
    overdue = "Overdue"
    cancelled = "Cancelled"


class PaymentMethod(str, enum.Enum):
    cash = "Cash"
    upi = "UPI"
    card = "Card"
    bank_transfer = "Bank Transfer"
    cheque = "Cheque"


class PaymentStatus(str, enum.Enum):
    success = "Success"
    failed = "Failed"
    pending = "Pending"


class FeeStructure(Base):
    __tablename__ = "fee_structures"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    fee_items = relationship("FeeItem", back_populates="fee_structure")
    invoices = relationship("Invoice", back_populates="fee_structure")


class FeeItem(Base):
    __tablename__ = "fee_items"

    id = Column(Integer, primary_key=True, index=True)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date)
    is_mandatory = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    fee_structure = relationship("FeeStructure", back_populates="fee_items")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"))
    invoice_number = Column(String(50), unique=True, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), default=0)
    due_amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.pending)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="invoices")
    fee_structure = relationship("FeeStructure", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    transaction_id = Column(String(100))
    receipt_number = Column(String(50))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.success)
    remarks = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    invoice = relationship("Invoice", back_populates="payments")
