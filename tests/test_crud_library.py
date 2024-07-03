from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
from .. import models, schemas
from app.actions import crud_library
from app.database import Base, get_db_session, engine

# Override database URL for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


# Dependency override to use a temporary database during testing
@pytest.fixture(scope="module")
def db_session():
    # Connect to the test database, create it, and initialize the schema
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    # Use a transaction for the tests, roll back afterward to keep the tests isolated
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
    # Create some test libraries
    for i in range(5):
        library_data = schemas.LibraryCreate(name=f"Library {i}")
        crud_library.create_library(db_session, library_data)

    # Retrieve libraries and check the count
    libraries = crud_library.get_libraries(db_session)
    assert len(libraries) == 5
