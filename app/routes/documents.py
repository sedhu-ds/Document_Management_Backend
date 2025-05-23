from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.dependencies import get_current_editor_or_admin_user , get_current_active_user, get_current_admin_user
from app import schemas
from app import models
from app.models import database
# from app.dependencies import get_current_active_user
from app import models
from fastapi import Depends


router = APIRouter(prefix="/documents", tags=["documents"])


# Create Document
@router.post("/", response_model=schemas.DocumentOut, status_code=status.HTTP_201_CREATED)
def create_document(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_editor_or_admin_user)

):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type")

    content = file.file.read().decode("utf-8")
    new_document = models.Document(
        title=file.filename,
        content=content,
        uploaded_by=current_user.id,
        uploaded_at=datetime.utcnow()
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


# Read All Documents
@router.get("/", response_model=List[schemas.DocumentOut])
def read_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return db.query(models.Document).offset(skip).limit(limit).all()


# Read Single Document
@router.get("/{document_id}", response_model=schemas.DocumentOut)
def read_document(
    document_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


# Update Document
@router.put("/{document_id}", response_model=schemas.DocumentOut)
def update_document(
    document_id: int,
    updated_doc: schemas.DocumentUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_editor_or_admin_user)
):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.title = updated_doc.title
    document.content = updated_doc.content
    db.commit()
    db.refresh(document)
    return document


# Delete Document
@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(document)
    db.commit()
    return
