from sqlalchemy.orm import Session
from .. import models, schemas


# Book CRUD Operations
def insert_book(db: Session, book: schemas.BookCreate):
    try:
        db_book = models.Book(
            title=book.title,
            author=book.author,
            ISBN=book.ISBN,
            publication_year=book.publication_year,
            library_id=book.library_id,
            is_available=book.is_available,
            average_rating=book.average_rating,
            ratings_count=book.ratings_count,
            language=book.language,
            page_count=book.page_count,
            description=book.description,
            publisher=book.publisher,
            categories=book.categories,
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except Exception as e:
        db.rollback()
        raise e


def add_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_book(db: Session, book: schemas.BookCreate, library_id: int):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        ISBN=book.ISBN,
        publication_year=book.publication_year,
        library_id=library_id,
        is_available=book.is_available,
    )
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


def get_all_books(db: Session):
    return db.query(models.Book).all()
