from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.core.dependencies import get_current_user, get_db

router = APIRouter()

# Get all users in MY tenant only
@router.get("/users")
def get_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only returns users from same tenant ✅
    users = db.query(User).filter(
        User.tenant_id == current_user.tenant_id
    ).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "tenant_id": u.tenant_id
        }
        for u in users
    ]

# Get my profile
@router.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "tenant_id": current_user.tenant_id
    }