from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import applications

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GRC NIST 800-171 Tool")

app.include_router(applications.router)

@app.get("/")
def root():
    return {"message": "GRC NIST 800-171 Tool API", "status": "ok"}

# Simple local auth stub (Phase 1)
@app.post("/auth/login")
def login(username: str, password: str):
    # Placeholder - will be replaced with real hash check
    return {"access_token": f"fake-token-for-{username}", "token_type": "bearer"}