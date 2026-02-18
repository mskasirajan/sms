from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.auth_schema import LoginRequest, TokenResponse, RefreshRequest, UserCreate, UserResponse, ChangePasswordRequest
from app.services import auth_service
from app.models.user import User

router = APIRouter()


def _normalize_role(name: str) -> str:
    """Convert role display name to snake_case token (e.g. 'School Admin' → 'school_admin')."""
    return name.lower().replace(' ', '_')


def _user_response(user: User) -> UserResponse:
    role_names = [r.name for r in user.roles]
    normalized = [_normalize_role(r) for r in role_names]
    return UserResponse(
        id=user.id,
        school_id=user.school_id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        is_active=user.is_active,
        role=normalized[0] if normalized else None,
        roles=normalized,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_tokens(db, payload.refresh_token)


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = auth_service.create_user(db, current_user.school_id, payload)
    return _user_response(user)


@router.post("/change-password", status_code=204)
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    auth_service.change_password(db, current_user, payload.current_password, payload.new_password)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return _user_response(current_user)
