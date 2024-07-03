from sqlalchemy.orm import Session
from app.actions import crud_librarian
from app.models import Librarian
from app.schemas import LibrarianCreate, LibrarianUpdate
from .utils import random_name


def test_add_librarian(db_session: Session):
    # Test adding a librarian
    librarian_data = {
        "name": random_name(),
        "email": "john.doe@example.com",
        "password": "password",
        "is_active": True,
    }
    new_librarian = crud_librarian.add_librarian(
        db_session, LibrarianCreate(**librarian_data)
    )
    assert new_librarian is not None
    assert new_librarian.name == librarian_data["name"]
    assert new_librarian.email == librarian_data["email"]
    assert new_librarian.is_active == librarian_data["is_active"]


def test_get_librarian(db_session: Session):
    # Test getting a librarian
    librarian_data = {
        "name": random_name(),
        "email": "jane.smith@example.com",
        "password": "password",
        "is_active": True,
    }
    new_librarian = crud_librarian.add_librarian(
        db_session, LibrarianCreate(**librarian_data)
    )
    assert new_librarian is not None
    librarian_id = new_librarian.librarian_id

    retrieved_librarian = crud_librarian.get_librarian(db_session, librarian_id)
    assert retrieved_librarian is not None
    assert retrieved_librarian.name == librarian_data["name"]
    assert retrieved_librarian.email == librarian_data["email"]
    assert retrieved_librarian.is_active == librarian_data["is_active"]


def test_update_librarian(db_session: Session):
    # Test updating a librarian
    librarian_data = {
        "name": random_name(),
        "email": "michael.brown@example.com",
        "password": "password",
        "is_active": True,
    }
    new_librarian = crud_librarian.add_librarian(
        db_session, LibrarianCreate(**librarian_data)
    )
    assert new_librarian is not None
    librarian_id = new_librarian.librarian_id

    updated_data = {
        "name": random_name(),
        "email": "updated.email@example.com",
        "is_active": False,
    }
    updated_librarian = crud_librarian.update_librarian(
        db_session, librarian_id, LibrarianUpdate(**updated_data)
    )
    assert updated_librarian is not None
    assert updated_librarian.name == updated_data["name"]
    assert updated_librarian.email == updated_data["email"]
    assert updated_librarian.is_active == updated_data["is_active"]


def test_remove_librarian(db_session: Session):
    # Test removing a librarian
    librarian_data = {
        "name": random_name(),
        "email": "emma.davis@example.com",
        "password": "password",
        "is_active": True,
    }
    new_librarian = crud_librarian.add_librarian(
        db_session, LibrarianCreate(**librarian_data)
    )
    assert new_librarian is not None
    librarian_id = new_librarian.librarian_id

    crud_librarian.remove_librarian(db_session, librarian_id)
    deleted_librarian = crud_librarian.get_librarian(db_session, librarian_id)
    assert deleted_librarian is None
