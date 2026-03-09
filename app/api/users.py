from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.dependencies import get_current_user, get_db
from app.core.roles import admin_only, manager_or_admin

router = APIRouter()

# Any logged in user
@router.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "tenant_id": current_user.tenant_id,
        "role": current_user.role
    }

# Manager or Admin only
@router.get("/users")
def get_users(
    current_user: User = Depends(manager_or_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(
        User.tenant_id == current_user.tenant_id
    ).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "tenant_id": u.tenant_id,
            "role": u.role
        }
        for u in users
    ]

# Admin only — update role
@router.put("/users/{user_id}/role")
def update_role(
    user_id: int,
    role: UserRole,
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == current_user.tenant_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role
    db.commit()
    db.refresh(user)
    return {"message": f"Role updated to {role}", "user_id": user_id}

# Admin only — delete user
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == current_user.tenant_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}