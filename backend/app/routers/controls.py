from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
import pandas as pd
from typing import List

router = APIRouter(prefix="/controls", tags=["controls"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.ControlOut])
def list_controls(db: Session = Depends(get_db)):
    return db.query(models.Control).all()

@router.get("/{control_id}", response_model=schemas.ControlOut)
def get_control(control_id: int, db: Session = Depends(get_db)):
    ctrl = db.query(models.Control).filter(models.Control.id == control_id).first()
    if not ctrl:
        raise HTTPException(status_code=404, detail="Control not found")
    return ctrl

@router.post("/import")
def import_controls_from_excel(excel_path: str = "NIST.SP.800-171_POAM_Blank_Template.xlsx", db: Session = Depends(get_db)):
    """
    Phase 1 implementation:
    - Parses the structure from the referenced Excel POAM template
    - Placeholder for pulling full control text + testing criteria from nist.gov
    """
    try:
        df = pd.read_excel(excel_path)
        imported = 0

        for _, row in df.iterrows():
            control_id = str(row.get("Control ID", "")).strip()
            if not control_id:
                continue

            existing = db.query(models.Control).filter(models.Control.control_id == control_id).first()
            if existing:
                continue

            new_control = models.Control(
                control_id=control_id,
                family=str(row.get("Family", "")),
                short_text=str(row.get("Control", ""))[:500],
                full_text=f"[NIST.gov enrichment pending] Full text for {control_id}",
                testing_criteria=f"[NIST.gov enrichment pending] Assessment criteria for {control_id}"
            )
            db.add(new_control)
            imported += 1

        db.commit()
        return {"message": f"Imported {imported} controls from Excel (NIST.gov enrichment placeholder active)"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")