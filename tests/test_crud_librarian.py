import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, schemas
from app.actions import crud_librarian
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


def test_add_librarian(db):
    librarian_data = schemas.LibrarianCreate(
        name="Test Librarian",
        address="123 Test St",
        phone_number="1234567890",
        library_id=1,
    )
    new_librarian = crud_librarian.add_librarian(db, librarian_data)
    assert new_librarian.name == "Test Librarian"
    assert new_librarian.address == "123 Test St"
    assert new_librarian.phone_number == "1234567890"
    assert new_librarian.library_id == 1
