import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.models.user import User, Role
from app.core.security import hash_password

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def seed_school_and_admin(db):
    from app.models.school import School
    school = School(name="Test School", code="TST001")
    db.add(school)
    db.flush()

    role = Role(name="School Admin", permissions="")
    db.add(role)
    db.flush()

    user = User(
        school_id=school.id,
        email="admin@test.com",
        hashed_password=hash_password("password123"),
        is_active=True,
    )
    user.roles = [role]
    db.add(user)
    db.commit()
    return {"school": school, "user": user, "role": role}


@pytest.fixture
def auth_headers(client, seed_school_and_admin):
    response = client.post("/auth/login", json={"email": "admin@test.com", "password": "password123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
