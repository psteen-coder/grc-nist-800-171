from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from datetime import datetime
from typing import List

router = APIRouter(prefix="/assessments", tags=["assessments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AssessmentOut)
def create_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    if assessment.status == models.StatusEnum.COMPLIANT and not assessment.evidence_blob:
        print(f"[TASK CREATED] Pending evidence required for control_id={assessment.control_id}")

    db_assess = models.Assessment(
        **assessment.dict(),
        assessed_at=datetime.utcnow()
    )
    db.add(db_assess)
    db.commit()
    db.refresh(db_assess)
    return db_assess

@router.get("/", response_model=List[schemas.AssessmentOut])
def list_assessments(db: Session = Depends(get_db)):
    return db.query(models.Assessment).all()

@router.get("/summary/{application_id}")
def assessment_summary(application_id: int, db: Session = Depends(get_db)):
    assessments = db.query(models.Assessment).filter(models.Assessment.application_id == application_id).all()
    total = len(assessments)
    compliant = len([a for a in assessments if a.status == models.StatusEnum.COMPLIANT])
    non_compliant = len([a for a in assessments if a.status != models.StatusEnum.COMPLIANT])

    return {
        "application_id": application_id,
        "total_controls_assessed": total,
        "compliant": compliant,
        "non_compliant_or_other": non_compliant,
        "compliance_percentage": round((compliant / total * 100), 1) if total > 0 else 0
    }