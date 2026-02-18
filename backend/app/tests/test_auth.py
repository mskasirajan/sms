from fastapi.testclient import TestClient


def test_login_success(client: TestClient, seed_school_and_admin):
    response = client.post("/auth/login", json={"email": "admin@test.com", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, seed_school_and_admin):
    response = client.post("/auth/login", json={"email": "admin@test.com", "password": "wrong"})
    assert response.status_code == 401


def test_login_unknown_email(client: TestClient, seed_school_and_admin):
    response = client.post("/auth/login", json={"email": "nobody@test.com", "password": "password123"})
    assert response.status_code == 401


def test_me_authenticated(client: TestClient, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert "School Admin" in data["roles"]


def test_me_unauthenticated(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_refresh_token(client: TestClient, seed_school_and_admin):
    login_resp = client.post("/auth/login", json={"email": "admin@test.com", "password": "password123"})
    refresh_token = login_resp.json()["refresh_token"]

    refresh_resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.json()


def test_change_password(client: TestClient, auth_headers):
    response = client.post(
        "/auth/change-password",
        json={"current_password": "password123", "new_password": "newpass456"},
        headers=auth_headers,
    )
    assert response.status_code == 204

    # Old password no longer works
    resp = client.post("/auth/login", json={"email": "admin@test.com", "password": "password123"})
    assert resp.status_code == 401

    # New password works
    resp = client.post("/auth/login", json={"email": "admin@test.com", "password": "newpass456"})
    assert resp.status_code == 200
