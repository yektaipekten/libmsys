from sqlalchemy.orm import Session
from .. import models, schemas

# Librarian CRUD Operations


def add_librarian(db: Session, librarian: schemas.LibrarianCreate):
    db_librarian = models.Librarian(**librarian.dict())
    db.add(db_librarian)
    db.commit()
    db.refresh(db_librarian)
    return db_librarian


def remove_librarian(db: Session, librarian_id: int):
    db_librarian = (
        db.query(models.Librarian)
        .filter(models.Librarian.librarian_id == librarian_id)
        .first()
    )
    if db_librarian:
        db.delete(db_librarian)
        db.commit()
    return db_librarian


def get_librarian(db: Session, librarian_id: int):
    return (
        db.query(models.Librarian)
        .filter(models.Librarian.librarian_id == librarian_id)
        .first()
    )


def update_librarian(
    db: Session, librarian_id: int, librarian_update: schemas.LibrarianUpdate
):
    db_librarian = (
        db.query(models.Librarian)
        .filter(models.Librarian.librarian_id == librarian_id)
        .first()
    )
    if db_librarian:
        update_data = librarian_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_librarian, key, value)
        db.commit()
        db.refresh(db_librarian)
    return db_librarian
