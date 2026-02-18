from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal
from app.models.fees import InvoiceStatus, PaymentMethod, PaymentStatus


class FeeItemCreate(BaseModel):
    name: str
    amount: Decimal
    due_date: Optional[date] = None
    is_mandatory: bool = True


class FeeStructureCreate(BaseModel):
    academic_year_id: int
    class_id: int
    name: str
    items: List[FeeItemCreate] = []


class FeeStructureResponse(BaseModel):
    id: int
    school_id: int
    academic_year_id: int
    class_id: int
    name: str

    model_config = {"from_attributes": True}


class InvoiceCreate(BaseModel):
    student_id: int
    academic_year_id: int
    fee_structure_id: int
    due_date: Optional[date] = None


class InvoiceResponse(BaseModel):
    id: int
    school_id: int
    invoice_number: str
    student_id: int
    total_amount: Decimal
    paid_amount: Decimal
    due_amount: Decimal
    status: str
    due_date: Optional[date]

    model_config = {"from_attributes": True}


class RecordPaymentRequest(BaseModel):
    invoice_id: int
    amount: Decimal
    payment_date: date
    payment_method: PaymentMethod
    transaction_id: Optional[str] = None
    remarks: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    school_id: int
    invoice_id: int
    student_id: int
    amount: Decimal
    payment_date: date
    payment_method: str
    transaction_id: Optional[str]
    receipt_number: Optional[str]
    status: str

    model_config = {"from_attributes": True}


class StudentFeeStatus(BaseModel):
    student_id: int
    student_name: str
    total_fees: Decimal
    paid_amount: Decimal
    due_amount: Decimal
    status: str
