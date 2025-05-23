from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models,db, dependencies
from typing import List
from app.models import database
from fastapi import Depends


router = APIRouter(prefix="/users", tags=["users"])


# Read all users
@router.get("/", response_model=List[schemas.UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_admin_user)
):
    return db.query(models.User).offset(skip).limit(limit).all()


# Read single user
@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_admin_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_admin_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for attr, value in user_data.dict(exclude_unset=True).items():
        setattr(user, attr, value)

    db.commit()
    db.refresh(user)
    return user


# Delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_admin_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
