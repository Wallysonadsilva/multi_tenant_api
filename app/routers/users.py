from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password, verify_password, create_jwt_token, create_refresh_token, decode_refresh_token
from app.auth_dependency import get_current_user
from app.schemas import LoginRequest, RefreshTokenRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_pw, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_jwt_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"}

@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "Welcome to the protected route!", "user": current_user}

@router.post("/refresh-token")
def refresh_access_token(request: RefreshTokenRequest):
    payload = decode_refresh_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # New access token
    new_access_token = create_jwt_token({"sub": payload["sub"]})
    return {"access_token": new_access_token, "token_type": "bearer"}