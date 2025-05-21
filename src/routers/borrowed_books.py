from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime
from ..schemas.schemas import BorrowedBook, BorrowedBookCreate
from ..models.models import BorrowedBook as BorrowedBookModel
from ..models.models import Book as BookModel
from ..models.models import Reader as ReaderModel
from ..database.database import get_db
from ..auth.auth import get_current_active_user

router = APIRouter()

@router.post("/borrow/", response_model=BorrowedBook)
def borrow_book(
    borrow: BorrowedBookCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Проверяем существование книги
    book = db.query(BookModel).filter(BookModel.id == borrow.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Проверяем количество доступных экземпляров (Бизнес-логика 1)
    if book.copies_available <= 0:
        raise HTTPException(
            status_code=400,
            detail="No copies of this book available"
        )
    
    # Проверяем существование читателя
    reader = db.query(ReaderModel).filter(ReaderModel.id == borrow.reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    # Проверяем количество книг у читателя (Бизнес-логика 2)
    active_borrows = db.query(BorrowedBookModel).filter(
        and_(
            BorrowedBookModel.reader_id == borrow.reader_id,
            BorrowedBookModel.return_date.is_(None)
        )
    ).count()
    
    if active_borrows >= 3:
        raise HTTPException(
            status_code=400,
            detail="Reader has already borrowed maximum number of books (3)"
        )
    
    # Создаем запись о выдаче
    db_borrow = BorrowedBookModel(**borrow.dict())
    
    # Уменьшаем количество доступных экземпляров
    book.copies_available -= 1
    
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    
    return db_borrow

@router.post("/return/{borrow_id}")
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Находим запись о выдаче
    borrow = db.query(BorrowedBookModel).filter(BorrowedBookModel.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    # Проверяем, не была ли книга уже возвращена (Бизнес-логика 3)
    if borrow.return_date is not None:
        raise HTTPException(
            status_code=400,
            detail="This book has already been returned"
        )
    
    # Обновляем запись о возврате
    borrow.return_date = datetime.utcnow()
    
    # Увеличиваем количество доступных экземпляров
    book = db.query(BookModel).filter(BookModel.id == borrow.book_id).first()
    book.copies_available += 1
    
    db.commit()
    
    return {"message": "Book returned successfully"}

@router.get("/borrowed-books/reader/{reader_id}", response_model=List[BorrowedBook])
def get_reader_borrowed_books(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Проверяем существование читателя
    reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    # Получаем список всех невозвращенных книг читателя
    borrowed_books = db.query(BorrowedBookModel).filter(
        and_(
            BorrowedBookModel.reader_id == reader_id,
            BorrowedBookModel.return_date.is_(None)
        )
    ).all()
    
    return borrowed_books

@router.get("/borrowed-books/", response_model=List[BorrowedBook])
def get_all_borrowed_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    borrowed_books = db.query(BorrowedBookModel).offset(skip).limit(limit).all()
    return borrowed_books
