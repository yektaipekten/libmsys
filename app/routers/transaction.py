import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models import (
    Book as SQLAlchemyBook,
    Member as SQLAlchemyMember,
    Transaction as SQLAlchemyTransaction,
)
from app.database import get_db_session
from app.actions import crud_transaction
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BorrowBookRequest(BaseModel):
    book_id: int
    member_id: int


@router.get("/availability/{book_id}")
async def check_availability(book_id: int, db: Session = Depends(get_db_session)):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.is_available:
        raise HTTPException(status_code=200, detail="The book is available.")
    return {
        "book_id": db_book.book_id,
        "title": db_book.title,
        "author": db_book.author,
        "ISBN": db_book.ISBN,
        "publication_year": db_book.publication_year,
        "library_id": db_book.library_id,
        "is_available": db_book.is_available,
    }


@router.post("/return/{book_id}/{member_id}")
async def return_book(
    book_id: int, member_id: int, db: Session = Depends(get_db_session)
):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if db_book.is_available:
        raise HTTPException(
            status_code=400, detail="The book is already returned to the library."
        )

    db_transaction, error = crud_transaction.return_book(db, book_id, member_id)
    if error:
        raise HTTPException(status_code=404, detail=error)

    db_book.is_available = True

    db.commit()
    db.refresh(db_transaction)
    db.refresh(db_book)

    return {
        "message": f"The book '{db_book.title}' (ID: {db_book.book_id}) has been returned by member (ID: {member_id}).",
        "book_id": db_book.book_id,
        "title": db_book.title,
        "is_available": db_book.is_available,
        "transaction": {
            "book_id": db_transaction.book_id,
            "member_id": db_transaction.member_id,
            "issue_date": db_transaction.issue_date,
            "return_date": db_transaction.return_date,
        },
    }


@router.post("/borrow_book")
async def borrow_book(
    request: BorrowBookRequest, db: Session = Depends(get_db_session)
):
    logger.info(f"Borrow book request received: {request}")

    db_book, db_member, error = crud_transaction.borrow_book(
        db, request.book_id, request.member_id
    )
    if error:
        logger.error(f"Error in borrowing book: {error}")
        raise HTTPException(status_code=400, detail=error)

    if db_book is None:
        logger.error("Book not found")
        raise HTTPException(status_code=404, detail="Book not found")

    if db_member is None:
        logger.error("Member not found")
        raise HTTPException(status_code=404, detail="Member not found")

    if not db_book.is_available:
        logger.warning("Book is already borrowed")
        return {"detail": "Book is already borrowed"}

    logger.info(f"Book borrowed successfully: {db_book.book_id}")
    return {
        "message": "Book borrowed successfully",
        "book": db_book,
        "member": db_member,
    }


@router.get("/show_borrowed_books")
async def show_borrowed_books(member_id: int, db: Session = Depends(get_db_session)):
    books = crud_transaction.show_borrowed_books(db, member_id)
    logger.info(f"Showing borrowed books for member_id: {member_id}")
    return books


@router.get("/show_returned_books")
async def show_returned_books(member_id: int, db: Session = Depends(get_db_session)):
    books = crud_transaction.show_returned_books(db, member_id)
    logger.info(f"Showing returned books for member_id: {member_id}")
    return books
