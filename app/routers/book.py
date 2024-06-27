from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Book as SQLAlchemyBook
from app.schemas import Book as PydanticBook
from app.database import get_db_session
from app import crud

router = APIRouter()


@router.get("/{book_id}/availability", response_model=PydanticBook)
async def check_availability(book_id: int, db: Session = Depends(get_db_session)):
    db_book = crud.check_availability(db, book_id)
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


@router.post("/{book_id}/return")
async def return_book(book_id: int, db: Session = Depends(get_db_session)):
    db_book = crud.return_book_availability(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "message": f"The book '{db_book.title}' with ID {db_book.book_id} has been returned."
    }
