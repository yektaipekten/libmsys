from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas, database

router = APIRouter()


@router.post("/create/", response_model=schemas.Library)
def create_library(
    library: schemas.LibraryCreate, db: Session = Depends(database.get_db)
):
    return crud.create_library(db=db, library=library)


@router.get("/read/", response_model=List[schemas.Library])
def read_libraries(
    skip: int = 0, limit: int = 20, db: Session = Depends(database.get_db)
):
    return crud.get_libraries(db, skip=skip, limit=limit)


@router.get("/{library_id}/read", response_model=schemas.Library)
def read_library(library_id: int, db: Session = Depends(database.get_db)):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library


@router.post("/{library_id}/add", response_model=schemas.Book)
def add_book(
    library_id: int, book: schemas.BookCreate, db: Session = Depends(database.get_db)
):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return crud.create_book(db=db, book=book, library_id=library_id)


@router.delete("/{library_id}/{book_id}/remove")
def remove_book(library_id: int, book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.library_id != library_id:
        raise HTTPException(
            status_code=404, detail="Book not found in the specified library"
        )
    crud.delete_book(db=db, book_id=book_id)
    return {"message": "Book removed"}


@router.post("/{library_id}/register/", response_model=schemas.Member)
def register_member(
    library_id: int,
    member: schemas.MemberCreate,
    db: Session = Depends(database.get_db),
):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return crud.create_member(db=db, member=member, library_id=library_id)


@router.post("/{book_id}/issue", response_model=schemas.Transaction)
def issue_book(
    library_id: int,
    book_id: int,
    member_id: int,
    db: Session = Depends(database.get_db),
):
    db_book = crud.get_book(db, book_id=book_id)
    db_member = crud.get_member(db, member_id=member_id)
    if db_book is None or db_member is None or db_book.library_id != library_id:
        raise HTTPException(
            status_code=404, detail="Book or member not found in the specified library"
        )
    return crud.issue_book(db=db, book_id=book_id, member_id=member_id)


@router.post("/{book_id}/return", response_model=schemas.Transaction)
def return_book(
    library_id: int,
    book_id: int,
    member_id: int,
    db: Session = Depends(database.get_db),
):
    db_book = crud.get_book(db, book_id=book_id)
    db_member = crud.get_member(db, member_id=member_id)
    if db_book is None or db_member is None or db_book.library_id != library_id:
        raise HTTPException(
            status_code=404, detail="Book or member not found in the specified library"
        )
    return crud.return_book(db=db, book_id=book_id, member_id=member_id)
