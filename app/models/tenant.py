from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    domain = Column(String)

    # Relationship to users
    users = relationship("User", back_populates="tenant")