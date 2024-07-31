from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LibraryBase(BaseModel):
    name: str
    address: str


class LibraryCreate(LibraryBase):
    pass


class Library(LibraryBase):
    library_id: int
    books: List["Book"] = []
    members: List["Member"] = []
    librarians: List["Librarian"] = []

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    ISBN: Optional[str] = None
    publication_year: Optional[int] = None
    is_available: bool
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None
    language: Optional[str] = None
    page_count: Optional[int] = None
    description: Optional[str] = None
    publisher: Optional[str] = None
    categories: Optional[str] = None
    library_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    book_id: int

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    name: str
    address: str
    phone_number: str


class MemberCreate(MemberBase):
    library_id: int


class Member(MemberBase):
    member_id: int
    library_id: int

    class Config:
        from_attributes = True


class LibrarianBase(BaseModel):
    name: str
    address: str
    phone_number: str


class LibrarianCreate(LibrarianBase):
    library_id: int


class LibrarianUpdate(LibrarianBase):
    pass


class Librarian(LibrarianBase):
    librarian_id: int
    library_id: int

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    book_id: int
    member_id: int
    issue_date: datetime
    return_date: datetime


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    transaction_id: int

    class Config:
        from_attributes = True


class BookRecommendation(BaseModel):
    book_id: int
    title: str
    author: str
    publication_year: int
    is_available: bool
    average_rating: float
    language: str
    page_count: int
    categories: str

    class Config:
        from_attributes = True
