from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import create_access_token
from app.core.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI
)
import httpx

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Step 1 — Redirect user to Google login page
@router.get("/auth/google")
def google_login():
    params = (
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return RedirectResponse(GOOGLE_AUTH_URL + params)

# Step 2 — Google redirects back here with a code
@router.get("/auth/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    
    # Exchange code for token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(GOOGLE_TOKEN_URL, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        })

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Google login failed")

    # Get user info from Google
    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

    user_info = user_info_response.json()
    email = user_info.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Could not get email from Google")

    # Check if user exists, if not create them
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            password="google-oauth-no-password",
            tenant_id=1  # Default tenant for Google users
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create JWT token
    jwt_token = create_access_token({
        "sub": user.email,
        "tenant_id": user.tenant_id
    })

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "email": email
    }