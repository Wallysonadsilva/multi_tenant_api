from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import hash_password, verify_password, create_jwt_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(password)
    new_user = models.User(email=email, hashed_password=hashed_pw, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def home():
    return {"message": "Welcome to Multi-tenant Saas API!"}