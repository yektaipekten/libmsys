from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Book as SQLAlchemyBook, Transaction as SQLAlchemyTransaction
from app.schemas import Transaction as PydanticTransaction
from app.database import get_db

router = APIRouter()


# totally trash
@router.get("/availability/{book_id}", response_model=PydanticTransaction)
async def check_availability(book_id: int, db: Session = Depends(get_db)):
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


@router.post("/return/{book_id}", response_model=PydanticTransaction)
async def return_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.is_available = True
    db.commit()
    db.refresh(db_book)

    transaction = SQLAlchemyTransaction(
        book_id=db_book.book_id,
        action="return",
        message=f"The book '{db_book.title}' with ID {db_book.book_id} has been returned.",
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction
