from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    # Relationship to tenant
    tenant = relationship("Tenant", back_populates="users")