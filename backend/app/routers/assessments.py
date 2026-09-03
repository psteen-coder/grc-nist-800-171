from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from datetime import datetime

router = APIRouter(prefix="/assessments", tags=["assessments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AssessmentOut)
def create_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    # Basic status rule enforcement
    if assessment.status == models.StatusEnum.COMPLIANT and not assessment.evidence_blob:
        # Create pending evidence task (simplified for now)
        print(f"[TASK] Pending evidence required for control {assessment.control_id}")

    db_assess = models.Assessment(
        **assessment.dict(),
        assessed_at=datetime.utcnow()
    )
    db.add(db_assess)
    db.commit()
    db.refresh(db_assess)
    return db_assess

@router.get("/", response_model=list[schemas.AssessmentOut])
def list_assessments(db: Session = Depends(get_db)):
    return db.query(models.Assessment).all()