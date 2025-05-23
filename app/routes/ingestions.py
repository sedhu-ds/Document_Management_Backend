from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, dependencies
from datetime import datetime
from app.models import database
from typing import List
from fastapi import Depends


router = APIRouter(prefix="/ingestions", tags=["ingestions"])


# Trigger ingestion
@router.post("/trigger/{document_id}", status_code=status.HTTP_202_ACCEPTED)
def trigger_ingestion(
    document_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_editor_or_admin_user)
):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    existing_ingestion = db.query(models.Ingestion).filter(
        models.Ingestion.document_id == document_id,
        models.Ingestion.status.in_(["in_progress", "completed"])
    ).first()

    if existing_ingestion:
        raise HTTPException(status_code=400, detail="Ingestion already triggered")

    new_ingestion = models.Ingestion(
        document_id=document_id,
        status="in_progress",
        started_at=datetime.utcnow()
    )
    db.add(new_ingestion)
    db.commit()
    db.refresh(new_ingestion)
    return {"message": "Ingestion triggered", "id": new_ingestion.id}


# Get all ingestions
@router.get("/", response_model=List[schemas.IngestionOut])
def read_ingestions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user)
):
    return db.query(models.Ingestion).offset(skip).limit(limit).all()


# Get a single ingestion
@router.get("/{ingestion_id}", response_model=schemas.IngestionOut)
def read_ingestion(
    ingestion_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user)
):
    ingestion = db.query(models.Ingestion).filter(models.Ingestion.id == ingestion_id).first()
    if not ingestion:
        raise HTTPException(status_code=404, detail="Ingestion not found")
    return ingestion


# Update ingestion (status)
@router.put("/{ingestion_id}", response_model=schemas.IngestionOut)
def update_ingestion(
    ingestion_id: int,
    ingestion_data: schemas.IngestionUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_editor_or_admin_user)
):
    ingestion = db.query(models.Ingestion).filter(models.Ingestion.id == ingestion_id).first()
    if not ingestion:
        raise HTTPException(status_code=404, detail="Ingestion not found")

    if ingestion_data.status:
        ingestion.status = ingestion_data.status

    db.commit()
    db.refresh(ingestion)
    return ingestion


# Delete ingestion
@router.delete("/{ingestion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingestion(
    ingestion_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_admin_user)
):
    ingestion = db.query(models.Ingestion).filter(models.Ingestion.id == ingestion_id).first()
    if not ingestion:
        raise HTTPException(status_code=404, detail="Ingestion not found")

    db.delete(ingestion)
    db.commit()
