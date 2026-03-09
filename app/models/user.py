from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    role = Column(Enum(UserRole), default=UserRole.employee)

    tenant = relationship("Tenant", back_populates="users")