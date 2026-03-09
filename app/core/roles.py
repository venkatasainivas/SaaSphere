from fastapi import Depends, HTTPException
from app.models.user import User, UserRole
from app.core.dependencies import get_current_user

def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

def manager_or_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(
            status_code=403,
            detail="Manager or Admin access required"
        )
    return current_user