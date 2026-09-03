from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/controls", tags=["controls"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ControlOut])
def list_controls(db: Session = Depends(get_db)):
    return db.query(models.Control).all()

@router.get("/{control_id}", response_model=schemas.ControlOut)
def get_control(control_id: int, db: Session = Depends(get_db)):
    ctrl = db.query(models.Control).filter(models.Control.id == control_id).first()
    if not ctrl:
        raise HTTPException(status_code=404, detail="Control not found")
    return ctrl

# Placeholder for import endpoint (Excel + NIST.gov enrichment)
@router.post("/import")
def import_controls(db: Session = Depends(get_db)):
    # TODO: Implement Excel parsing + NIST.gov enrichment
    return {"message": "Control import endpoint ready (Phase 1 placeholder)"}