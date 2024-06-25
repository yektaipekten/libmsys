from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import (
    Book as SQLAlchemyBook,
    Member as SQLAlchemyMember,
    Transaction as SQLAlchemyTransaction,
)
from app.LibrarySchema import Book as PydanticBook, Member as PydanticMember
from app.database import get_db_session

router = APIRouter()


@router.post("/{book_id}/{member_id}")
async def borrow_book(
    book_id: int, member_id: int, db: Session = Depends(get_db_session)
):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member_id)
        .first()
    )
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    if not db_book.is_available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    db_book.is_available = False
    db.commit()
    db.refresh(db_book)

    transaction = SQLAlchemyTransaction(
        book_id=db_book.book_id, member_id=db_member.member_id, action="borrowed"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return {
        "message": f"The book '{db_book.title}' has been borrowed by '{db_member.name}'."
    }


@router.post("/{book_id}/return")
async def return_book(book_id: int, db: Session = Depends(get_db_session)):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.is_available = True
    db.commit()
    db.refresh(db_book)

    return {
        "message": f"The book '{db_book.title}' with ID {db_book.book_id} has been returned."
    }

    transaction = SQLAlchemyTransaction(
        book_id=db_book.book_id, member_id=db_member.member_id, action="returned"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return {
        "message": f"The book '{db_book.title}' has been returned by '{db_member.name}'."
    }


@router.get("/{member_id}/borrowed")
async def show_borrowed_books(member_id: int, db: Session = Depends(get_db_session)):
    db_books = (
        db.query(SQLAlchemyTransaction)
        .filter(
            SQLAlchemyTransaction.member_id == member_id,
            SQLAlchemyTransaction.action == "borrowed",
        )
        .all()
    )
    if not db_books:
        raise HTTPException(
            status_code=404, detail="No borrowed books found for this member"
        )

    return db_books


@router.get("/{member_id}/returned")
async def show_returned_books(member_id: int, db: Session = Depends(get_db_session)):
    db_books = (
        db.query(SQLAlchemyTransaction)
        .filter(
            SQLAlchemyTransaction.member_id == member_id,
            SQLAlchemyTransaction.action == "returned",
        )
        .all()
    )
    if not db_books:
        raise HTTPException(
            status_code=404, detail="No returned books found for this member"
        )

    return db_books


@router.get("/{member_id}/info")
async def show_member_info(member_id: int, db: Session = Depends(get_db_session)):
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member_id)
        .first()
    )
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return db_member


@router.get("/{book_id}", response_model=PydanticBook)
async def check_availability(book_id: int, db: Session = Depends(get_db_session)):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "book_id": db_book.book_id,
        "title": db_book.title,
        "author": db_book.author,
        "ISBN": db_book.ISBN,
        "publication_year": db_book.publication_year,
        "library_id": db_book.library_id,
        "is_available": db_book.is_available,
    }
