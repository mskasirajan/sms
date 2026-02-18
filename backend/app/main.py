from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import get_logger
from app.routers import (
    auth_router,
    student_router,
    teacher_router,
    attendance_router,
    fees_router,
    exam_router,
)

logger = get_logger(__name__)

app = FastAPI(
    title="School Management System API",
    description="REST API for School Management System — Phase 1 MVP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(student_router.router, prefix="/students", tags=["Students"])
app.include_router(teacher_router.router, prefix="/teachers", tags=["Teachers"])
app.include_router(attendance_router.router, prefix="/attendance", tags=["Attendance"])
app.include_router(fees_router.router, prefix="/fees", tags=["Fees & Billing"])
app.include_router(exam_router.router, prefix="/exams", tags=["Exams & Report Cards"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "SMS API v1.0.0"}
