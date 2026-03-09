from pydantic import BaseModel
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: str
    password: str
    tenant_id: int = 1
    role: UserRole = UserRole.employee

class UserResponse(BaseModel):
    id: int
    email: str
    tenant_id: int
    role: UserRole

    class Config:
        from_attributes = True