from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.fees import FeeStructure, FeeItem, Invoice, Payment, InvoiceStatus
from app.models.student import Student
from app.schemas.fees_schema import FeeStructureCreate, InvoiceCreate, RecordPaymentRequest
from decimal import Decimal
import uuid
from datetime import date


def _next_invoice_number(db: Session, school_id: int) -> str:
    count = db.query(Invoice).filter(Invoice.school_id == school_id).count()
    return f"INV-{school_id:04d}-{count + 1:06d}"


def _next_receipt_number(db: Session, school_id: int) -> str:
    count = db.query(Payment).filter(Payment.school_id == school_id).count()
    return f"RCP-{school_id:04d}-{count + 1:06d}"


def create_fee_structure(db: Session, school_id: int, payload: FeeStructureCreate) -> FeeStructure:
    structure = FeeStructure(
        school_id=school_id,
        academic_year_id=payload.academic_year_id,
        class_id=payload.class_id,
        name=payload.name,
    )
    db.add(structure)
    db.flush()

    for item_data in payload.items:
        item = FeeItem(fee_structure_id=structure.id, **item_data.model_dump())
        db.add(item)

    db.commit()
    db.refresh(structure)
    return structure


def get_fee_structures(db: Session, school_id: int, academic_year_id: int = None):
    query = db.query(FeeStructure).filter(FeeStructure.school_id == school_id)
    if academic_year_id:
        query = query.filter(FeeStructure.academic_year_id == academic_year_id)
    return query.all()


def create_invoice(db: Session, school_id: int, payload: InvoiceCreate) -> Invoice:
    student = db.query(Student).filter(
        Student.id == payload.student_id, Student.school_id == school_id
    ).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    # Calculate total from fee structure items
    total = Decimal("0.00")
    if payload.fee_structure_id:
        structure = db.query(FeeStructure).filter(FeeStructure.id == payload.fee_structure_id).first()
        if structure:
            total = sum(item.amount for item in structure.fee_items if item.is_mandatory)

    invoice = Invoice(
        school_id=school_id,
        student_id=payload.student_id,
        academic_year_id=payload.academic_year_id,
        fee_structure_id=payload.fee_structure_id,
        invoice_number=_next_invoice_number(db, school_id),
        total_amount=total,
        paid_amount=Decimal("0.00"),
        due_amount=total,
        due_date=payload.due_date,
        status=InvoiceStatus.pending,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def record_payment(db: Session, school_id: int, payload: RecordPaymentRequest) -> Payment:
    invoice = db.query(Invoice).filter(
        Invoice.id == payload.invoice_id, Invoice.school_id == school_id
    ).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    if invoice.status == InvoiceStatus.paid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invoice already paid")
    if payload.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment amount must be positive")
    if payload.amount > invoice.due_amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount exceeds due balance")

    payment = Payment(
        school_id=school_id,
        invoice_id=invoice.id,
        student_id=invoice.student_id,
        amount=payload.amount,
        payment_date=payload.payment_date,
        payment_method=payload.payment_method,
        transaction_id=payload.transaction_id,
        receipt_number=_next_receipt_number(db, school_id),
        remarks=payload.remarks,
    )
    db.add(payment)

    invoice.paid_amount += payload.amount
    invoice.due_amount -= payload.amount
    if invoice.due_amount <= 0:
        invoice.status = InvoiceStatus.paid
    else:
        invoice.status = InvoiceStatus.partial

    db.commit()
    db.refresh(payment)
    return payment


def get_student_fee_status(db: Session, school_id: int, student_id: int):
    student = db.query(Student).filter(
        Student.id == student_id, Student.school_id == school_id
    ).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    invoices = db.query(Invoice).filter(
        Invoice.student_id == student_id, Invoice.school_id == school_id
    ).all()

    total = sum(inv.total_amount for inv in invoices)
    paid = sum(inv.paid_amount for inv in invoices)
    due = sum(inv.due_amount for inv in invoices)

    overall_status = "Paid" if due == 0 and total > 0 else ("Partial" if paid > 0 else "Pending")
    return {
        "student_id": student.id,
        "student_name": f"{student.first_name} {student.last_name}",
        "total_fees": total,
        "paid_amount": paid,
        "due_amount": due,
        "status": overall_status,
    }
