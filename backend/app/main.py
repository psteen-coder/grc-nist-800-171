from fastapi import FastAPI
from .database import engine, Base
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GRC NIST 800-171 Tool")

@app.get("/")
def root():
    return {"message": "GRC NIST 800-171 Tool API", "status": "ok"}