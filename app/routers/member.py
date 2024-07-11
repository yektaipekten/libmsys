from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import Book as PydanticBook, Member as PydanticMember
from app.database import get_db_session
from app import crud

from app import recommendation

router = APIRouter()


@router.post("/{book_id}/{member_id}")
async def borrow_book(
    book_id: int, member_id: int, db: Session = Depends(get_db_session)
):
    db_book, db_member, error = crud.borrow_book(db, book_id, member_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {
        "message": f"The book '{db_book.title}' has been borrowed by '{db_member.name}'."
    }


@router.post("/{book_id}/return")
async def return_book(
    book_id: int, member_id: int, db: Session = Depends(get_db_session)
):
    db_book, error = crud.return_book(db, book_id, member_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {
        "message": f"The book '{db_book.title}' with ID {db_book.book_id} has been returned."
    }


@router.get("/{member_id}/borrowed")
async def show_borrowed_books(member_id: int, db: Session = Depends(get_db_session)):
    db_books = crud.show_borrowed_books(db, member_id)
    if not db_books:
        raise HTTPException(
            status_code=404, detail="No borrowed books found for this member"
        )
    return db_books


@router.get("/{member_id}/returned")
async def show_returned_books(member_id: int, db: Session = Depends(get_db_session)):
    db_books = crud.show_returned_books(db, member_id)
    if not db_books:
        raise HTTPException(
            status_code=404, detail="No returned books found for this member"
        )
    return db_books


@router.get("/{member_id}/info")
async def show_member_info(member_id: int, db: Session = Depends(get_db_session)):
    db_member = crud.show_member_info(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.get("/{book_id}", response_model=PydanticBook)
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


@router.get("/{member_id}/recommendations")
async def get_recommendations(member_id: int, db: Session = Depends(get_db_session)):
    recommendations_df = recommendation.hybrid_recommendations(member_id, db)
    if recommendations_df.empty:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return recommendations_df.to_dict("records")
