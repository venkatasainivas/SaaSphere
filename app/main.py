from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import tenant, user
from app.api import tenants
from app.api import auth                    

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SaaSphere API")

app.include_router(tenants.router)
app.include_router(auth.router)            