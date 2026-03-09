from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    tenant_id: int = 1      # default value

class UserLogin(BaseModel):
    email: str
    password: str