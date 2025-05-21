from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    publication_year: Optional[int] = Field(None, gt=1000, lt=datetime.now().year + 2)
    isbn: Optional[str] = Field(None)
    copies_available: int = Field(1, ge=0)
    description: Optional[str] = Field(None, max_length=1000)

    @validator('isbn')
    def validate_isbn(cls, v):
        if v is not None:
            v = v.replace('-', '')
            if not (len(v) == 10 or len(v) == 13):
                raise ValueError('ISBN must be 10 or 13 characters long')
        return v

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class ReaderBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    id: int

    class Config:
        from_attributes = True

class BorrowedBookBase(BaseModel):
    book_id: int
    reader_id: int

class BorrowedBookCreate(BorrowedBookBase):
    pass

class BorrowedBook(BorrowedBookBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    @validator('return_date')
    def validate_return_date(cls, v, values):
        if v is not None and 'borrow_date' in values and v < values['borrow_date']:
            raise ValueError('Return date cannot be earlier than borrow date')
        return v

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
