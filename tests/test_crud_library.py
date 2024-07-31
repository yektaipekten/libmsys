from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
from app import models, schemas
from app.actions import crud_library
from app.database import Base, get_db_session, engine

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:ipekten@localhost/sample"


@pytest.fixture(scope="module")
def db_session():
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def test_create_library(db_session: Session):
    library_data = schemas.LibraryCreate(name="Test Library")
    created_library = crud_library.create_library(db_session, library_data)
    assert created_library.name == "Test Library"


def test_get_library(db_session: Session):
    library_data = schemas.LibraryCreate(name="Test Library")
    created_library = crud_library.create_library(db_session, library_data)
    retrieved_library = crud_library.get_library(db_session, created_library.library_id)
    assert retrieved_library.name == "Test Library"


def test_get_libraries(db_session: Session):
    for i in range(5):
        library_data = schemas.LibraryCreate(name=f"Library {i}")
        crud_library.create_library(db_session, library_data)

    libraries = crud_library.get_libraries(db_session)
    assert len(libraries) == 5
