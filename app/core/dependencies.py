from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.core.security import decode_token
from app.db.database import SessionLocal
from app.models.user import User

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        email: str = payload.get("sub")
        tenant_id: int = payload.get("tenant_id")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        if user.tenant_id != tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_tenant(current_user: User = Depends(get_current_user)):
    return current_user.tenant_id