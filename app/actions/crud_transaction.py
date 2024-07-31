import logging
from sqlalchemy.orm import Session
from .. import models
from datetime import datetime
from app.models import (
    Book as SQLAlchemyBook,
    Member as SQLAlchemyMember,
    Transaction as SQLAlchemyTransaction,
)

# Set Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Transaction Operations


def issue_book(db: Session, book_id: int, member_id: int):
    logger.info(
        f"Issuing book with ID {book_id} to member with ID {member_id}"
    )  # Logger
    db_transaction = models.Transaction(book_id=book_id, member_id=member_id)
    db.query(models.Book).filter(models.Book.book_id == book_id).update(
        {"is_available": False}
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    logger.info(f"Book with ID {book_id} issued to member with ID {member_id}")
    return db_transaction


def return_book(db: Session, book_id: int, member_id: int):
    db_transaction = (
        db.query(SQLAlchemyTransaction)
        .filter(
            SQLAlchemyTransaction.book_id == book_id,
            SQLAlchemyTransaction.member_id == member_id,
        )
        .order_by(SQLAlchemyTransaction.issue_date.desc())
        .first()
    )
    if db_transaction:
        db_transaction.return_date = datetime.utcnow()
        db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).update(
            {"is_available": True}
        )
        db.commit()
        db.refresh(db_transaction)
        return db_transaction, None
    else:
        return None, "No active borrow transaction found for this book and member."


def borrow_book(db: Session, book_id: int, member_id: int):
    logger.info(
        f"Member with ID {member_id} attempting to borrow book with ID {book_id}"
    )
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    db_member = (
        db.query(models.Member).filter(models.Member.member_id == member_id).first()
    )
    if db_book is None:
        logger.error(f"Book with ID {book_id} not found")
        return None, None, "Book not found"
    if db_member is None:
        logger.error(f"Member with ID {member_id} not found")
        return None, None, "Member not found"
    if not db_book.is_available:
        logger.warning(f"Book with ID {book_id} is already borrowed")
        return db_book, db_member, "Book is already borrowed"

    db_book.is_available = False
    db.commit()
    db.refresh(db_book)

    transaction = models.Transaction(
        book_id=db_book.book_id, member_id=db_member.member_id, action="borrowed"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    logger.info(f"Book with ID {book_id} borrowed by member with ID {member_id}")

    return db_book, db_member, None


def show_borrowed_books(db: Session, member_id: int):
    logger.info(f"Fetching borrowed books for member with ID {member_id}")
    db_books = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.member_id == member_id,
            models.Transaction.action == "borrowed",
        )
        .all()
    )
    return db_books


def show_returned_books(db: Session, member_id: int):
    logger.info(f"Fetching returned books for member with ID {member_id}")
    db_books = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.member_id == member_id,
            models.Transaction.action == "returned",
        )
        .all()
    )
    return db_books
