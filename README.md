# SaaSphere — Multi-Tenant SaaS Backend Platform

A production-ready multi-tenant SaaS backend built with FastAPI.

## Tech Stack
- FastAPI
- PostgreSQL + SQLAlchemy
- Alembic Migrations
- JWT Authentication
- OAuth2 Google Login
- Redis Caching
- Role Based Permissions

## Features
- Multi-tenant architecture with data isolation
- JWT authentication with tenant context
- Google OAuth2 login
- Role based permissions (Admin/Manager/Employee)
- Redis caching for performance
- Database migrations with Alembic

## Setup
```bash
# Clone repo
git clone https://github.com/venkatasainivas/SaaSphere.git
cd saasphere

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

## API Docs
http://127.0.0.1:8000/docs
