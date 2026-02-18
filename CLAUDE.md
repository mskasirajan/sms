# CLAUDE.md — School Management System (SMS) Repository

## Overview

This repository is a **design and architecture blueprint** for a Modern School Management System (SMS/ERP). It contains no runnable application code — all files are static HTML documents that serve as planning references, technical blueprints, and database schemas intended to guide the eventual implementation.

The system is designed to be a cloud-based, mobile-first, multi-tenant SaaS platform connecting students, parents, teachers, and administrators.

---

## Repository Structure

```
sms/
├── sms.html                          # Comprehensive SMS blueprint (primary reference)
├── design.html                       # ER diagram + PostgreSQL schema + FastAPI structure
├── school_management_modernization.html  # Architecture + module + API design document
├── .gitignore                        # Node.js standard gitignore
└── CLAUDE.md                         # This file
```

### File Descriptions

#### `sms.html` — Comprehensive Application Blueprint
The primary overview document covering:
- **Objective**: Replace manual processes with a digital ecosystem
- **Modernization Principles**: Mobile-first, cloud-first, RBAC, automation, security, modular design, AI/analytics
- **User Roles & RBAC**: Admin, Principal, Teachers, Parents, Students, Support Staff (Transport Manager, Librarian, Accountant, Hostel Manager)
- **Architecture overview**: Frontend → API Gateway → Modules → PostgreSQL + Storage + Notifications
- **19 Modules** organized across 5 categories (Core, Learning, Facilities, Communication, Advanced)
- **Tech stack recommendations**
- **Security & compliance requirements**
- **Deployment architecture**
- **4-phase implementation roadmap**

#### `design.html` — Technical Design Blueprint
Deep technical reference containing:
- **ER Diagram** (text-based): All entity relationships across modules
- **Full PostgreSQL DDL schema**: `CREATE TABLE` scripts for all tables (schools, users, roles, students, teachers, parents, staff, attendance, fees, invoices, payments, exams, marks, homework, transport, notifications, etc.)
- **FastAPI backend folder structure**: Production-ready layout with `app/core/`, `app/models/`, `app/schemas/`, `app/routers/`, `app/services/`, `app/utils/`, `app/tests/`
- **Sample code snippets**: `main.py`, student router, auth router

#### `school_management_modernization.html` — Architecture Document
Concise architecture reference covering:
- High-level architecture layers
- Technology stack
- Module groupings (Core, Operations, Finance, Facilities, Communication, Analytics)
- RBAC roles list (9 roles including Super Admin)
- Database schema table listing
- Sample REST API endpoints
- Security features checklist
- AI features list
- Deployment architecture
- 4-phase implementation roadmap

---

## Designed Technology Stack

| Layer | Technology |
|---|---|
| Frontend Web | React / Next.js |
| Mobile App | React Native / Flutter |
| Backend API | FastAPI (Python) or .NET Core |
| Database | PostgreSQL |
| Cache | Redis (optional) |
| File Storage | AWS S3 / Azure Blob |
| Push Notifications | Firebase |
| Notifications | SMS, Email, WhatsApp Business API |
| Hosting | AWS / Azure |
| CI/CD | GitHub Actions / Azure DevOps |
| Container | Docker (Kubernetes for scale) |

---

## System Modules

### Core Modules (Phase 1 MVP)
1. **Student Management** — Admissions, profiles, class allocation, documents
2. **Staff & Teacher Management** — Profiles, qualifications, class assignments
3. **Attendance Management** — Daily attendance, RFID/Face/QR support, parent alerts
4. **Timetable Management** — Class/teacher/room scheduling
5. **Fees & Billing** — Fee structures, UPI/card payments, auto receipts, due alerts
6. **Exams & Report Cards** — Exam scheduling, marks entry, grade calculation, PDF reports

### Learning & Engagement Modules (Phase 2)
7. **Homework & Assignments** — Upload, submission, teacher feedback
8. **Learning Materials / Content Hub** — Notes, PPT, PDFs, video links
9. **Online Exams** (optional) — MCQ, auto-evaluation, anti-cheat

### Facility & Operations Modules (Phase 3)
10. **Transport Management** — GPS live tracking, routes, pickup/drop notifications
11. **Library Management** — Book catalog, issue/return, fines, reservations
12. **Hostel Management** — Room allocation, meal tracking, hostel fees
13. **Inventory Management** — Uniforms, books, stationery, lab equipment

### Communication Modules
14. **Notifications & Alerts** — SMS/Email/Push/WhatsApp
15. **Announcements & Circulars** — School-wide or class-specific, read receipts
16. **Parent-Teacher Communication** — Chat, office hours, meeting scheduling

### Advanced Modules (Phase 4)
17. **Analytics Dashboard** — Attendance trends, performance, fee collection
18. **AI & Predictive Insights** — Student risk prediction, slow learner detection
19. **Multi-School SaaS Support** — Data isolation, subscription billing, custom branding

---

## Database Schema

The database uses **PostgreSQL** with a multi-tenant design (every table includes `school_id`).

### Key Table Groups

**Master / Setup Tables**
- `schools`, `academic_years`, `classes`, `sections`, `subjects`

**User & Auth Tables**
- `users`, `roles`, `user_roles`
- Profile tables: `students`, `teachers`, `parents`, `staff`
- `student_parent_mapping`

**Academic Tables**
- `student_class_history`, `student_subject_mapping`

**Attendance Tables**
- `attendance_sessions`, `student_attendance`
- Status values: `Present`, `Absent`, `Late`, `Half-Day`

**Fees Tables**
- `fee_structures`, `fee_items`, `invoices`, `payments`, `receipts_pdf_storage`

**Exam Tables**
- `exams`, `exam_schedule`, `marks`, `report_cards`

**Homework Tables**
- `homework`, `homework_submission`, `attachments`

**Transport Tables**
- `vehicles`, `routes`, `student_route_mapping`, `gps_logs`

**Notification Tables**
- `notifications`, `notification_logs`
- Channels: `SMS`, `Email`, `WhatsApp`, `Push`

---

## Planned API Design (REST)

```
POST /auth/login
POST /auth/refresh
POST /auth/logout

GET  /students
POST /students
PUT  /students/{id}
GET  /students/{id}/profile

POST /attendance/session
POST /attendance/mark
GET  /attendance/report

POST /fees/invoice/create
POST /fees/payment
GET  /fees/student/{id}/status

POST /exams/create
POST /exams/marks/upload
GET  /exams/reportcard/{studentId}
```

---

## RBAC Roles

| Role | Key Permissions |
|---|---|
| Super Admin | Full system access across all schools |
| School Admin | Student records, fees, staff, system configuration |
| Principal | Monitor academics, approve circulars, view dashboards |
| Teacher | Mark attendance, upload homework, enter marks, communicate |
| Accountant | Fees management, payment reports |
| Librarian | Book catalog, issue/return tracking |
| Transport Manager | Vehicles, routes, GPS monitoring |
| Student | View timetable, submit homework, access materials |
| Parent | Track attendance, pay fees, receive notifications |

---

## Security Requirements

- JWT Authentication with Refresh Token
- Password hashing using bcrypt
- OTP login for parents
- Role-based API authorization (enforced at both API and UI level)
- Audit logs for admin changes
- Database encryption for sensitive columns
- Automatic backup and restore plan
- Rate limiting for login endpoints
- File scanning for malicious uploads

---

## Backend Folder Structure (FastAPI)

When implementing the FastAPI backend, follow this structure:

```
school-erp-backend/
├── app/
│   ├── main.py                 # FastAPI app entry point, router registration
│   ├── core/
│   │   ├── config.py           # Environment settings
│   │   ├── security.py         # JWT helpers
│   │   ├── database.py         # DB session/connection
│   │   └── logger.py
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic request/response schemas
│   ├── routers/                # API route definitions
│   ├── services/               # Business logic layer
│   ├── utils/                  # PDF generator, email/SMS/WhatsApp senders
│   └── tests/                  # pytest test files
├── requirements.txt
├── Dockerfile
└── README.md
```

**Convention**: Each module has a matching model, schema, router, and service file (e.g., `student.py`, `student_schema.py`, `student_router.py`, `student_service.py`).

---

## Implementation Roadmap

| Phase | Focus |
|---|---|
| Phase 1 (MVP) | Student management, teacher management, attendance, basic fees, notifications |
| Phase 2 (Growth) | Homework/assignments, timetable, exams/marks, report cards, parent app |
| Phase 3 (Advanced) | Transport + GPS, library, hostel, inventory, analytics dashboard |
| Phase 4 (Premium) | AI insights engine, multi-school SaaS, subscription billing, custom branding |

---

## Conventions for AI Assistants

- **This repo is a blueprint repo**: All current content is HTML documentation, not running code. When adding implementation code, create appropriate subdirectories (`backend/`, `frontend/`, `database/`) rather than placing code at the root.
- **Multi-tenant by design**: Every database query and API endpoint must filter by `school_id`. JWT tokens must carry `school_id` in their claims.
- **Modular architecture**: Keep modules independent. Avoid tight coupling between modules — use events/notifications for cross-module communication.
- **HTML files are reference documents**: Do not refactor or convert the existing HTML blueprints. They are design artifacts, not templates.
- **PostgreSQL conventions**: Use `SERIAL PRIMARY KEY`, foreign key constraints, and `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` for audit fields. Amount columns use `NUMERIC(10,2)`.
- **Security is non-negotiable**: Never expose raw passwords, never skip RBAC checks, always validate file uploads.
- **Report exports**: All reports must support both PDF and Excel export formats.
- **No time estimates**: Focus on what needs to be done rather than time projections.
