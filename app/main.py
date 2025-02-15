from fastapi import FastAPI
from app.routers import users
from app.database import engine

app = FastAPI()

from app.database import Base
Base.metadata.create_all(bind=engine)

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Multi-tenant Saas API!"}