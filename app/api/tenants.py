from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tenants")
def create_tenant(data: TenantCreate, db: Session = Depends(get_db)):
    tenant = Tenant(name=data.name, domain=data.domain)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant