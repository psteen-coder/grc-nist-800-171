from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import applications, controls, assessments, users, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GRC NIST 800-171 Tool")

app.include_router(applications.router)
app.include_router(controls.router)
app.include_router(assessments.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "GRC NIST 800-171 Tool API", "status": "ok"}