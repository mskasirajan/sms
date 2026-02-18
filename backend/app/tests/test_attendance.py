from fastapi.testclient import TestClient
from datetime import date


def _create_teacher(client, auth_headers, school_id):
    from app.models.teacher import Teacher
    # Use API
    resp = client.post(
        "/teachers",
        json={"employee_id": "EMP-001", "first_name": "Teacher", "last_name": "One"},
        headers=auth_headers,
    )
    return resp.json()["id"]


def _create_student(client, auth_headers, admission_no="ADM-001"):
    resp = client.post(
        "/students",
        json={"admission_no": admission_no, "first_name": "Student", "last_name": "One"},
        headers=auth_headers,
    )
    return resp.json()["id"]


def test_mark_attendance(client: TestClient, auth_headers, seed_school_and_admin):
    teacher_id = _create_teacher(client, auth_headers, seed_school_and_admin["school"].id)
    student_id = _create_student(client, auth_headers)

    response = client.post(
        "/attendance/session",
        json={
            "class_id": 1,
            "teacher_id": teacher_id,
            "date": str(date.today()),
            "period": 1,
            "records": [
                {"student_id": student_id, "status": "Present"}
            ],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["teacher_id"] == teacher_id


def test_duplicate_attendance_session(client: TestClient, auth_headers, seed_school_and_admin):
    teacher_id = _create_teacher(client, auth_headers, seed_school_and_admin["school"].id)
    student_id = _create_student(client, auth_headers)

    payload = {
        "class_id": 1,
        "teacher_id": teacher_id,
        "date": str(date.today()),
        "period": 1,
        "records": [{"student_id": student_id, "status": "Present"}],
    }
    client.post("/attendance/session", json=payload, headers=auth_headers)
    response = client.post("/attendance/session", json=payload, headers=auth_headers)
    assert response.status_code == 409


def test_attendance_report(client: TestClient, auth_headers, seed_school_and_admin):
    teacher_id = _create_teacher(client, auth_headers, seed_school_and_admin["school"].id)
    student_id = _create_student(client, auth_headers)

    client.post(
        "/attendance/session",
        json={
            "class_id": 1,
            "teacher_id": teacher_id,
            "date": str(date.today()),
            "period": 1,
            "records": [{"student_id": student_id, "status": "Absent"}],
        },
        headers=auth_headers,
    )

    response = client.post(
        "/attendance/report",
        json={
            "class_id": 1,
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    report = response.json()
    assert len(report) == 1
    assert report[0]["absent"] == 1
    assert report[0]["attendance_percentage"] == 0.0
