from pydantic import BaseModel
from typing import Optional, List
from datetime import date


# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    ISBN: str
    publication_year: int
    is_available: bool
    library_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    ISBN: Optional[str] = None
    publication_year: Optional[int] = None
    is_available: Optional[bool] = None
    library_id: Optional[int] = None


class Book(BookBase):
    id: int

    class Config:
        orm_mode: True


# Library Schemas
class LibraryBase(BaseModel):
    name: str
    address: str


class LibraryCreate(LibraryBase):
    pass


class LibraryUpdate(LibraryBase):
    name: Optional[str] = None
    address: Optional[str] = None


class Library(LibraryBase):
    id: int

    class Config:
        orm_mode: True


# Member Schemas
class MemberBase(BaseModel):
    name: str
    email: str


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    name: Optional[str] = None
    email: Optional[str] = None


class Member(MemberBase):
    id: int

    class Config:
        orm_mode: True


# Librarian Schemas
class LibrarianBase(BaseModel):
    name: str
    library_id: int


class LibrarianCreate(LibrarianBase):
    pass


class LibrarianUpdate(LibrarianBase):
    name: Optional[str] = None
    library_id: Optional[int] = None


class Librarian(LibrarianBase):
    id: int

    class Config:
        orm_mode: True


# Transaction Schemas
class TransactionBase(BaseModel):
    book_id: int
    member_id: int
    borrow_date: date
    return_date: Optional[date]


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    book_id: Optional[int] = None
    member_id: Optional[int] = None
    borrow_date: Optional[date] = None
    return_date: Optional[date] = None


class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode: True
