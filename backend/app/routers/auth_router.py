from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.auth_schema import LoginRequest, TokenResponse, RefreshRequest, UserCreate, UserResponse, ChangePasswordRequest
from app.services import auth_service
from app.models.user import User

router = APIRouter()


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
    return UserResponse(
        id=user.id,
        school_id=user.school_id,
        email=user.email,
        phone=user.phone,
        is_active=user.is_active,
        roles=[r.name for r in user.roles],
    )


@router.post("/change-password", status_code=204)
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    auth_service.change_password(db, current_user, payload.current_password, payload.new_password)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        school_id=current_user.school_id,
        email=current_user.email,
        phone=current_user.phone,
        is_active=current_user.is_active,
        roles=[r.name for r in current_user.roles],
    )
