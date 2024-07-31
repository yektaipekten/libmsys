from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal, engine
from app import models, schemas
from app.actions import crud_member

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
    yield
    models.Base.metadata.drop_all(bind=engine)


def test_create_member(db_session: Session):
    member_data = schemas.MemberCreate(
        name="Test Member",
        email="test_member@example.com",
        library_id=1,
    )
    new_member = crud_member.create_member(db_session, member_data)
    assert new_member.name == "Test Member"
    assert new_member.email == "test_member@example.com"


def test_get_member(db_session: Session):
    member_data = schemas.MemberCreate(
        name="Test Member",
        email="test_member@example.com",
        library_id=1,
    )
    new_member = crud_member.create_member(db_session, member_data)
    fetched_member = crud_member.get_member(db_session, new_member.member_id)
    assert fetched_member.name == new_member.name
    assert fetched_member.email == new_member.email


def test_update_member(db_session: Session):
    member_data = schemas.MemberCreate(
        name="Test Member",
        email="test_member@example.com",
        library_id=1,
    )
    new_member = crud_member.create_member(db_session, member_data)
    updated_data = schemas.MemberUpdate(name="Updated Member")
    updated_member = crud_member.update_member(
        db_session, new_member.member_id, updated_data
    )
    assert updated_member.name == "Updated Member"


def test_delete_member(db_session: Session):
    member_data = schemas.MemberCreate(
        name="Test Member",
        email="test_member@example.com",
        library_id=1,
    )
    new_member = crud_member.create_member(db_session, member_data)
    crud_member.delete_member(db_session, new_member.member_id)
    fetched_member = crud_member.get_member(db_session, new_member.member_id)
    assert fetched_member is None
