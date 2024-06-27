from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from app.models import (
    Book as SQLAlchemyBook,
    Member as SQLAlchemyMember,
    Transaction as SQLAlchemyTransaction,
)
from app.schemas import (
    Book as PydanticBook,
    Member as PydanticMember,
    Transaction as PydanticTransaction,
)


# Book
def create_book(db: Session, book: schemas.BookCreate, library_id: int):
    book.model_dump(exclude={"library_id"})
    db_book = models.Book(**book.model_dump, library_id=library_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def delete_book(db: Session, book_id: int):
    db.query(models.Book).filter(models.Book.book_id == book_id).delete()
    db.commit()


def create_member(db: Session, member: schemas.MemberCreate, library_id: int):
    member_data = member.dict()
    member_data.pop("library_id", None)
    db_member = models.Member(**member_data, library_id=library_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()


def issue_book(db: Session, book_id: int, member_id: int):
    db_transaction = models.Transaction(book_id=book_id, member_id=member_id)
    db.query(models.Book).filter(models.Book.book_id == book_id).update(
        {"is_available": False}
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def return_book(db: Session, book_id: int):
    db_transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.book_id == book_id)
        .order_by(models.Transaction.issue_date.desc())
        .first()
    )
    if db_transaction:
        db_transaction.return_date = datetime.utcnow()
        db.query(models.Book).filter(models.Book.book_id == book_id).update(
            {"is_available": True}
        )
        db.commit()
        db.refresh(db_transaction)
    return db_transaction


def get_library(db: Session, library_id: int):
    return (
        db.query(models.Library).filter(models.Library.library_id == library_id).first()
    )


def get_libraries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Library).offset(skip).limit(limit).all()


def create_library(db: Session, library: schemas.LibraryCreate):
    db_library = models.Library(**library.dict())
    db.add(db_library)
    db.commit()
    db.refresh(db_library)
    return db_library


def check_availability(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def return_book_availability(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if db_book:
        db_book.is_available = True
        db.commit()
        db.refresh(db_book)
    return db_book


# Librarian
def add_librarian(db: Session, librarian: schemas.LibrarianCreate):
    db_librarian = models.Librarian(**librarian.dict())
    db.add(db_librarian)
    db.commit()
    db.refresh(db_librarian)
    return db_librarian


def remove_librarian(db: Session, librarian_id: int):
    db_librarian = (
        db.query(models.Librarian)
        .filter(models.Librarian.librarian_id == librarian_id)
        .first()
    )
    if db_librarian:
        db.delete(db_librarian)
        db.commit()
    return db_librarian


def add_book(db: Session, book: schemas.Book):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def remove_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def add_member(db: Session, member: schemas.Member):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def remove_member(db: Session, member_id: int):
    db_member = (
        db.query(models.Member).filter(models.Member.member_id == member_id).first()
    )
    if db_member:
        db.delete(db_member)
        db.commit()
    return db_member


def show_member_info(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()


def issue_book_to_member(db: Session, book_id: int, member_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    db_member = (
        db.query(models.Member).filter(models.Member.member_id == member_id).first()
    )

    if db_book and db_member and db_book.is_available:
        db_book.is_available = False
        db.commit()
        db.refresh(db_book)
    return db_book, db_member


def return_book_from_member(db: Session, book_id: int, member_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    db_member = (
        db.query(models.Member).filter(models.Member.member_id == member_id).first()
    )

    if db_book and db_member:
        db_book.is_available = True
        db.commit()
        db.refresh(db_book)
    return db_book, db_member


# Member
def borrow_book(db: Session, book_id: int, member_id: int):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member_id)
        .first()
    )
    if db_book is None:
        return None, None, "Book not found"
    if db_member is None:
        return None, None, "Member not found"
    if not db_book.is_available:
        return db_book, db_member, "Book is already borrowed"

    db_book.is_available = False
    db.commit()
    db.refresh(db_book)

    transaction = SQLAlchemyTransaction(
        book_id=db_book.book_id, member_id=db_member.member_id, action="borrowed"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return db_book, db_member, None


def return_book(db: Session, book_id: int, member_id: int):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        return None, "Book not found"

    db_book.is_available = True
    db.commit()
    db.refresh(db_book)

    transaction = SQLAlchemyTransaction(
        book_id=db_book.book_id, member_id=member_id, action="returned"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return db_book, None


def show_borrowed_books(db: Session, member_id: int):
    db_books = (
        db.query(SQLAlchemyTransaction)
        .filter(
            SQLAlchemyTransaction.member_id == member_id,
            SQLAlchemyTransaction.action == "borrowed",
        )
        .all()
    )
    return db_books


def show_returned_books(db: Session, member_id: int):
    db_books = (
        db.query(SQLAlchemyTransaction)
        .filter(
            SQLAlchemyTransaction.member_id == member_id,
            SQLAlchemyTransaction.action == "returned",
        )
        .all()
    )
    return db_books


def show_member_info(db: Session, member_id: int):
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member_id)
        .first()
    )
    return db_member


# Transaction


def check_availability(db: Session, book_id: int):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    return db_book


def check_availability(db: Session, book_id: int):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    return db_book


def return_book(db: Session, book_id: int):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        return None, "Book not found"

    if db_book.is_available:
        return db_book, "The book already returned to the library."

    db_book.is_available = True
    db.commit()
    db.refresh(db_book)

    return db_book, None
