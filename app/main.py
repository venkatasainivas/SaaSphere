from fastapi import FastAPI

app = FastAPI(title="SaaSphere API")

@app.get("/")
def root():
    return {"message": "Welcome to SaaSphere"}


from app.db.database import Base, engine
from app.models import tenant, user

Base.metadata.create_all(bind=engine)

from app.api import tenants

app.include_router(tenants.router)