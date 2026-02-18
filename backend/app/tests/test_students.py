from fastapi.testclient import TestClient


def test_create_student(client: TestClient, auth_headers, seed_school_and_admin, db):
    response = client.post(
        "/students",
        json={
            "admission_no": "ADM-001",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "gender": "Male",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["admission_no"] == "ADM-001"
    assert data["first_name"] == "Ravi"


def test_create_student_duplicate_admission_no(client: TestClient, auth_headers):
    payload = {"admission_no": "ADM-001", "first_name": "Ravi", "last_name": "Kumar"}
    client.post("/students", json=payload, headers=auth_headers)
    response = client.post("/students", json=payload, headers=auth_headers)
    assert response.status_code == 409


def test_list_students(client: TestClient, auth_headers):
    # Create two students
    for i in range(2):
        client.post(
            "/students",
            json={"admission_no": f"ADM-00{i}", "first_name": f"Student{i}", "last_name": "Test"},
            headers=auth_headers,
        )
    response = client.get("/students", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_student(client: TestClient, auth_headers):
    create_resp = client.post(
        "/students",
        json={"admission_no": "ADM-001", "first_name": "Priya", "last_name": "Sharma"},
        headers=auth_headers,
    )
    student_id = create_resp.json()["id"]
    response = client.get(f"/students/{student_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == student_id


def test_get_student_not_found(client: TestClient, auth_headers):
    response = client.get("/students/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_student(client: TestClient, auth_headers):
    create_resp = client.post(
        "/students",
        json={"admission_no": "ADM-001", "first_name": "Priya", "last_name": "Sharma"},
        headers=auth_headers,
    )
    student_id = create_resp.json()["id"]
    update_resp = client.put(
        f"/students/{student_id}",
        json={"first_name": "Priyanka"},
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["first_name"] == "Priyanka"


def test_delete_student(client: TestClient, auth_headers):
    create_resp = client.post(
        "/students",
        json={"admission_no": "ADM-001", "first_name": "Delete", "last_name": "Me"},
        headers=auth_headers,
    )
    student_id = create_resp.json()["id"]
    del_resp = client.delete(f"/students/{student_id}", headers=auth_headers)
    assert del_resp.status_code == 204

    get_resp = client.get(f"/students/{student_id}", headers=auth_headers)
    assert get_resp.status_code == 404
