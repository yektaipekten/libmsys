from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Book as SQLAlchemyBook, Member as SQLAlchemyMember
from app.LibrarySchema import Book as PydanticBook, Member as PydanticMember

from app.database import get_db_session

router = APIRouter()


@router.post("/add")  # Add book to lib
async def add_book(book: PydanticBook, db: Session = Depends(get_db_session)):
    db_book = SQLAlchemyBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"message": f"The book '{db_book.title}' has been added."}


@router.post("/remove/{book_id}")  # Remove book to lib
async def remove_book(book_id: int, db: Session = Depends(get_db_session)):
    db_book = db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"message": f"The book '{db_book.title}' has been removed."}


@router.post("/members")
async def add_member(member: PydanticMember, db: Session = Depends(get_db_session)):
    db_member = SQLAlchemyMember(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return {"message": f"The member '{db_member.name}' has been added."}


@router.delete("/members/{member_id}")
async def remove_member(member_id: int, db: Session = Depends(get_db_session)):
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member_id)
        .first()
    )
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(db_member)
    db.commit()
    return {"message": f"The member '{db_member.name}' has been removed."}


@router.get("/members/{member_id}")
async def show_member_info(member_id: int, db: Session = Depends(get_db_session)):
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member_id)
        .first()
    )
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return db_member


@router.post("/books/{book_id}/issue")
async def issue_book(
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
    return {
        "message": f"The book '{db_book.title}' has been issued to {db_member.name}."
    }


@router.post("/books/{book_id}/return")
async def return_book(
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

    db_book.is_available = True

    db.commit()
    db.refresh(db_book)
    return {
        "message": f"The book '{db_book.title}' has been returned by {db_member.name}."
    }
