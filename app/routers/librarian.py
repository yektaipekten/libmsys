from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import Book as PydanticBook, Member as PydanticMember
from app.schemas import LibrarianCreate as PydanticLibrarianCreate
from app.database import get_db_session
from app import crud

router = APIRouter()


@router.post("/librarians/add")
async def add_librarian(
    librarian: PydanticLibrarianCreate, db: Session = Depends(get_db_session)
):
    db_librarian = crud.add_librarian(db, librarian)
    return {"message": f"The librarian '{db_librarian.name}' has been added."}


@router.delete("/librarians/remove")
async def remove_librarian(librarian_id: int, db: Session = Depends(get_db_session)):
    db_librarian = crud.remove_librarian(db, librarian_id)
    if db_librarian is None:
        raise HTTPException(status_code=404, detail="Librarian not found")
    return {"message": f"The librarian '{db_librarian.name}' has been removed."}


@router.post("/books/add")  # Add book to lib
async def add_book(book: PydanticBook, db: Session = Depends(get_db_session)):
    db_book = crud.add_book(db, book)
    return {"message": f"The book '{db_book.title}' has been added."}


@router.delete("/books/remove/{book_id}")  # Remove book from lib
async def remove_book(book_id: int, db: Session = Depends(get_db_session)):
    db_book = crud.remove_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"The book '{db_book.title}' has been removed."}


@router.post("/members/add")
async def add_member(member: PydanticMember, db: Session = Depends(get_db_session)):
    db_member = crud.add_member(db, member)
    return {"message": f"The member '{db_member.name}' has been added."}


@router.delete("/members/remove/{member_id}")
async def remove_member(member_id: int, db: Session = Depends(get_db_session)):
    db_member = crud.remove_member(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": f"The member '{db_member.name}' has been removed."}


@router.get("/members/{member_id}")
async def show_member_info(member_id: int, db: Session = Depends(get_db_session)):
    db_member = crud.show_member_info(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.post("/books/{book_id}/issue")
async def issue_book(
    book_id: int, member_id: int, db: Session = Depends(get_db_session)
):
    db_book, db_member = crud.issue_book_to_member(db, book_id, member_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    if not db_book.is_available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")
    return {
        "message": f"The book '{db_book.title}' has been issued to {db_member.name}."
    }


@router.post("/books/{book_id}/return")
async def return_book(
    book_id: int, member_id: int, db: Session = Depends(get_db_session)
):
    db_book, db_member = crud.return_book_from_member(db, book_id, member_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {
        "message": f"The book '{db_book.title}' has been returned by {db_member.name}."
    }
