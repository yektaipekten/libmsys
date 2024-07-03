from sqlalchemy.orm import Session
from .. import models
from datetime import datetime

# Transaction Operations


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


def borrow_book(db: Session, book_id: int, member_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    db_member = (
        db.query(models.Member).filter(models.Member.member_id == member_id).first()
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

    transaction = models.Transaction(
        book_id=db_book.book_id, member_id=db_member.member_id, action="borrowed"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return db_book, db_member, None


def show_borrowed_books(db: Session, member_id: int):
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
    db_books = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.member_id == member_id,
            models.Transaction.action == "returned",
        )
        .all()
    )
    return db_books
