"""
Seed script — creates a default school, roles, and admin user.
Run from the backend/ directory:
    python seed.py
"""
from app.core.database import SessionLocal
from app.models.school import School
from app.models.user import User, Role
from app.core.security import hash_password

ROLES = [
    "Super Admin",
    "School Admin",
    "Principal",
    "Teacher",
    "Accountant",
    "Librarian",
    "Transport Manager",
    "Student",
    "Parent",
]

ADMIN_EMAIL = "admin@school.com"
ADMIN_PASSWORD = "Admin@123"


def seed():
    db = SessionLocal()
    try:
        # Skip if already seeded
        if db.query(School).first():
            print("Database already seeded. Skipping.")
            return

        # Create school
        school = School(
            name="Demo School",
            code="DEMO001",
            address="123 Main Street, City",
            phone="9000000000",
            email="school@demo.com",
        )
        db.add(school)
        db.flush()

        # Create roles
        roles = {}
        for role_name in ROLES:
            role = Role(name=role_name, permissions="")
            db.add(role)
            db.flush()
            roles[role_name] = role

        # Create admin user
        admin = User(
            school_id=school.id,
            email=ADMIN_EMAIL,
            hashed_password=hash_password(ADMIN_PASSWORD),
            full_name="School Administrator",
            is_active=True,
            is_verified=True,
        )
        admin.roles = [roles["School Admin"]]
        db.add(admin)
        db.commit()

        print("Seed complete!")
        print(f"  School : {school.name} (id={school.id})")
        print(f"  Email  : {ADMIN_EMAIL}")
        print(f"  Password: {ADMIN_PASSWORD}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
