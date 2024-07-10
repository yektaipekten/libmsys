from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal, engine
from app import models, schemas
from app.actions import crud_transaction

import pytest


@pytest.fixture(scope="module")
def db_session():
    """
    Fixture for creating a test database session.
    """
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown(db_session):
    """
    Fixture for setting up and tearing down the test database.
    """
    models.Base.metadata.create_all(bind=engine)

    library = models.Library(name="Test Library", address="123 Library St")
    db_session.add(library)
    db_session.commit()
    db_session.refresh(library)

    book = models.Book(
        title="Test Book",
        author="Author A",
        ISBN="1234567890",
        library_id=library.library_id,
        is_available=True,
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    member = models.Member(
        name="John Doe", email="john.doe@example.com", library_id=library.library_id
    )
    db_session.add(member)
    db_session.commit()
    db_session.refresh(member)

    yield

    models.Base.metadata.drop_all(bind=engine)


def test_issue_book(db_session: Session):
    book_id = db_session.query(models.Book).filter_by(ISNB="1234567890").first().book_id
    member_id = (
        db_session.query(models.Member)
        .filter_by(email="john.doe@example.com")
        .first()
        .member_id
    )

    transaction = crud_transaction.issue_book(db_session, book_id, member_id)
    assert transaction.book_id == book_id
    assert transaction.member_id == member_id
    assert (
        not db_session.query(models.Book)
        .filter(models.Book.book_id == book_id)
        .first()
        .is_available
    )


def test_return_book(db_session: Session):
    book_id = db_session.query(models.Book).filter_by(ISNB="1234567890").first().book_id

    transaction = crud_transaction.return_book(db_session, book_id)
    assert transaction.book_id == book_id
    assert transaction.return_date is not None
    assert (
        db_session.query(models.Book)
        .filter(models.Book.book_id == book_id)
        .first()
        .is_available
    )


def test_borrow_book(db_session: Session):
    new_book = models.Book(
        title="Another Test Book",
        author="Author B",
        ISNB="0987654321",
        library_id=1,
        is_available=True,
    )
    db_session.add(new_book)
    db_session.commit()
    db_session.refresh(new_book)

    new_member = models.Member(
        name="Jane Doe", email="jane.doe@example.com", library_id=1
    )
    db_session.add(new_member)
    db_session.commit()
    db_session.refresh(new_member)

    book_id = new_book.book_id
    member_id = new_member.member_id
    borrowed_book, borrowing_member, error = crud_transaction.borrow_book(
        db_session, book_id, member_id
    )
    assert borrowed_book.book_id == book_id
    assert borrowing_member.member_id == member_id
    assert error is None
    assert not borrowed_book.is_available

    borrowed_book, borrowing_member, error = crud_transaction.borrow_book(
        db_session, book_id, member_id
    )
    assert error == "Book is already borrowed"


def test_show_borrowed_books(db_session: Session):
    member_id = (
        db_session.query(models.Member)
        .filter_by(email="john.doe@example.com")
        .first()
        .member_id
    )
    borrowed_books = crud_transaction.show_borrowed_books(db_session, member_id)
    assert len(borrowed_books) > 0
    for transaction in borrowed_books:
        assert transaction.member_id == member_id
        assert transaction.action == "borrowed"


def test_show_returned_books(db_session: Session):
    member_id = (
        db_session.query(models.Member)
        .filter_by(email="john.doe@example.com")
        .first()
        .member_id
    )
    returned_books = crud_transaction.show_returned_books(db_session, member_id)
    assert len(returned_books) > 0
    for transaction in returned_books:
        assert transaction.member_id == member_id
        assert transaction.action == "returned"
