from sqlalchemy.orm import Session
from .. import models, schemas
from app.models import Library
from app.schemas import LibraryCreate

# Library CRUD Operations


def get_library(db: Session, library_id: int):
    return (
        db.query(models.Library).filter(models.Library.library_id == library_id).first()
    )


def get_libraries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Library).offset(skip).limit(limit).all()


def create_library(db: Session, library: schemas.LibraryCreate):
    db_library = models.Library(**library.dict())
    db.add(db_library)
    db.commit()
    db.refresh(db_library)
    return db_library
