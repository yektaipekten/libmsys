from sqlalchemy.orm import Session
from . import models, schemas


# Book Operations
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


# Transaction Operations
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transaction(db: Session, transaction_id: int):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )


def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Transaction).offset(skip).limit(limit).all()


def update_transaction(
    db: Session, transaction_id: int, transaction: schemas.TransactionUpdate
):
    db_transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if db_transaction:
        for key, value in transaction.dict(exclude_unset=True).items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int):
    db_transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction


# Member Operations
def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_members(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Member).offset(skip).limit(limit).all()


def update_member(db: Session, member_id: int, member: schemas.MemberUpdate):
    db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if db_member:
        for key, value in member.dict(exclude_unset=True).items():
            setattr(db_member, key, value)
        db.commit()
        db.refresh(db_member)
    return db_member


def delete_member(db: Session, member_id: int):
    db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if db_member:
        db.delete(db_member)
        db.commit()
    return db_member


# Librarian Operations
def create_librarian(db: Session, librarian: schemas.LibrarianCreate):
    db_librarian = models.Librarian(**librarian.dict())
    db.add(db_librarian)
    db.commit()
    db.refresh(db_librarian)
    return db_librarian


def get_librarian(db: Session, librarian_id: int):
    return (
        db.query(models.Librarian).filter(models.Librarian.id == librarian_id).first()
    )


def get_librarians(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Librarian).offset(skip).limit(limit).all()


def update_librarian(
    db: Session, librarian_id: int, librarian: schemas.LibrarianUpdate
):
    db_librarian = (
        db.query(models.Librarian).filter(models.Librarian.id == librarian_id).first()
    )
    if db_librarian:
        for key, value in librarian.dict(exclude_unset=True).items():
            setattr(db_librarian, key, value)
        db.commit()
        db.refresh(db_librarian)
    return db_librarian


def delete_librarian(db: Session, librarian_id: int):
    db_librarian = (
        db.query(models.Librarian).filter(models.Librarian.id == librarian_id).first()
    )
    if db_librarian:
        db.delete(db_librarian)
        db.commit()
    return db_librarian
