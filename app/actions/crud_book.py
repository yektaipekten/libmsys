from sqlalchemy.orm import Session
from .. import models, schemas

# Book CRUD Operations


def add_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_book(db: Session, book: schemas.BookCreate, library_id: int):
    db_book = models.Book(**book.dict(), library_id=library_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def delete_book(db: Session, book_id: int):
    db.query(models.Book).filter(models.Book.book_id == book_id).delete()
    db.commit()


def check_availability(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def return_book_availability(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if db_book:
        db_book.is_available = True
        db.commit()
        db.refresh(db_book)
    return db_book
