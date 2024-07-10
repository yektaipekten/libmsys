import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, schemas
from app.actions import crud_book, crud_library
from app.database import Base

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:ipekten@localhost/sample"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db():
    """Provide a clean database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_book(db):
    library_data = schemas.LibraryCreate(name="Test Library", address="123 Test St")
    new_library = crud_library.add_library(db, library_data)
    library_id = new_library.library_id

    book_data = schemas.BookCreate(
        title="Test Book",
        author="Author",
        ISNB="1234567890",
        publication_year=2020,
        is_available=True,
        library_id=library_id,
    )
    new_book = crud_book.create_book(db, book_data, library_id)
    assert new_book.title == "Test Book"
    assert new_book.author == "Author"
    assert new_book.ISBN == "1234567890"
    assert new_book.publication_year == 2020
    assert new_book.is_available
    assert new_book.library_id == library_id
