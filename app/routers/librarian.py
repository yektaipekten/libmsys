from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db_session

router = APIRouter(
    prefix="/librarians",
    tags=["librarians"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Librarian)
def create_librarian(
    librarian: schemas.LibrarianCreate, db: Session = Depends(get_db_session)
):
    return crud.create_librarian(db, librarian)


@router.get("/{librarian_id}", response_model=schemas.Librarian)
def read_librarian(librarian_id: int, db: Session = Depends(get_db_session)):
    db_librarian = crud.get_librarian(db, librarian_id)
    if db_librarian is None:
        raise HTTPException(status_code=404, detail="Librarian not found")
    return db_librarian


@router.get("/", response_model=list[schemas.Librarian])
def read_librarians(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)
):
    librarians = crud.get_librarians(db, skip=skip, limit=limit)
    return librarians


@router.put("/{librarian_id}", response_model=schemas.Librarian)
def update_librarian(
    librarian_id: int,
    librarian: schemas.LibrarianUpdate,
    db: Session = Depends(get_db_session),
):
    db_librarian = crud.update_librarian(db, librarian_id, librarian)
    if db_librarian is None:
        raise HTTPException(status_code=404, detail="Librarian not found")
    return db_librarian


@router.delete("/{librarian_id}", response_model=schemas.Librarian)
def delete_librarian(librarian_id: int, db: Session = Depends(get_db_session)):
    db_librarian = crud.delete_librarian(db, librarian_id)
    if db_librarian is None:
        raise HTTPException(status_code=404, detail="Librarian not found")
    return db_librarian
