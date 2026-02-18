The Phase 1 MVP backend is complete. Here's what was created — **49 files, 3,114 lines**:

```
backend/
├── app/
│   ├── main.py                         # FastAPI entry point + CORS
│   ├── core/
│   │   ├── config.py                   # Pydantic settings (.env)
│   │   ├── database.py                 # SQLAlchemy session
│   │   ├── security.py                 # JWT auth, RBAC dependency
│   │   └── logger.py
│   ├── models/                         # SQLAlchemy ORM (7 modules)
│   ├── schemas/                        # Pydantic v2 schemas (6 modules)
│   ├── routers/                        # REST endpoints (6 modules)
│   ├── services/                       # Business logic (6 modules)
│   ├── utils/
│   │   ├── pdf_generator.py            # ReportLab report card PDF
│   │   └── notifications.py           # SMS / Email / WhatsApp / Push stubs
│   └── tests/
│       ├── conftest.py                 # SQLite test DB + fixtures
│       ├── test_auth.py
│       ├── test_students.py
│       └── test_attendance.py
├── alembic/
│   └── versions/001_initial_schema.py  # Full DDL migration
├── requirements.txt
├── Dockerfile
└── .env.example
```

**Key features implemented:**
- JWT auth with access + refresh tokens; `school_id` embedded in every token
- All queries filtered by `school_id` (multi-tenant)
- RBAC via `require_roles()` dependency on sensitive endpoints
- Fee invoice → payment workflow with status tracking (Pending → Partial → Paid)
- Exam marks upload with automatic grade + report card generation (with rank calculation)
- Attendance session with duplicate prevention + summary report
- Auto-grade scale: A+ (≥90) down to F (<40)

**To run:**
```bash
cp .env.example .env   # set DATABASE_URL
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```