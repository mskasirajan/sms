from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.fees_schema import (
    FeeStructureCreate, FeeStructureResponse,
    InvoiceCreate, InvoiceResponse,
    RecordPaymentRequest, PaymentResponse,
    StudentFeeStatus,
)
from app.services import fees_service
from app.models.user import User

router = APIRouter()


# --- Fee Structures ---

@router.post("/structures", response_model=FeeStructureResponse, status_code=201)
def create_fee_structure(
    payload: FeeStructureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Accountant")),
):
    return fees_service.create_fee_structure(db, current_user.school_id, payload)


@router.get("/structures", response_model=List[FeeStructureResponse])
def list_fee_structures(
    academic_year_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return fees_service.get_fee_structures(db, current_user.school_id, academic_year_id)


# --- Invoices ---

@router.post("/invoice/create", response_model=InvoiceResponse, status_code=201)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Accountant")),
):
    return fees_service.create_invoice(db, current_user.school_id, payload)


# --- Payments ---

@router.post("/payment", response_model=PaymentResponse, status_code=201)
def record_payment(
    payload: RecordPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("School Admin", "Accountant")),
):
    return fees_service.record_payment(db, current_user.school_id, payload)


# --- Student Fee Status ---

@router.get("/student/{student_id}/status", response_model=StudentFeeStatus)
def student_fee_status(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return fees_service.get_student_fee_status(db, current_user.school_id, student_id)
