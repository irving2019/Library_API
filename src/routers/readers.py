from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas.schemas import Reader, ReaderCreate
from ..models.models import Reader as ReaderModel
from ..database.database import get_db
from ..auth.auth import get_current_active_user

router = APIRouter()

@router.post("/readers/", response_model=Reader)
def create_reader(
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_reader = db.query(ReaderModel).filter(ReaderModel.email == reader.email).first()
    if db_reader:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_reader = ReaderModel(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.get("/readers/", response_model=List[Reader])
def read_readers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    readers = db.query(ReaderModel).offset(skip).limit(limit).all()
    return readers

@router.get("/readers/{reader_id}", response_model=Reader)
def read_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    return db_reader

@router.put("/readers/{reader_id}", response_model=Reader)
def update_reader(
    reader_id: int,
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    for key, value in reader.dict().items():
        setattr(db_reader, key, value)
    
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.delete("/readers/{reader_id}")
def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    db.delete(db_reader)
    db.commit()
    return {"message": "Reader deleted successfully"}
