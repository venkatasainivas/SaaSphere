from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.dependencies import get_current_user, get_db
from app.core.roles import admin_only, manager_or_admin
from app.core.cache import get_cache, set_cache, delete_cache, clear_tenant_cache

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

# Manager or Admin — with Redis caching
@router.get("/users")
def get_users(
    current_user: User = Depends(manager_or_admin),
    db: Session = Depends(get_db)
):
    # Check cache first
    cache_key = f"tenant:{current_user.tenant_id}:users"
    cached = get_cache(cache_key)

    if cached:
        print("✅ Returning from Redis cache")
        return cached

    # If not in cache — hit database
    print("🔄 Fetching from database")
    users = db.query(User).filter(
        User.tenant_id == current_user.tenant_id
    ).all()

    result = [
        {
            "id": u.id,
            "email": u.email,
            "tenant_id": u.tenant_id,
            "role": u.role
        }
        for u in users
    ]

    # Save to Redis cache for 5 minutes
    set_cache(cache_key, result, expire=300)

    return result

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

    # Clear cache when data changes
    clear_tenant_cache(current_user.tenant_id)
    print("🗑️ Cache cleared after role update")

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

    # Clear cache when data changes
    clear_tenant_cache(current_user.tenant_id)
    print("🗑️ Cache cleared after user deletion")

    return {"message": "User deleted successfully"}