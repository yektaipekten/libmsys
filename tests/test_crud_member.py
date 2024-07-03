from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.database import SessionLocal, engine
from app import models, schemas, crud_member

import pytest


# Setup and Teardown
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


# Unit Tests


def test_create_member(db_session):
    member_data = schemas.MemberCreate(name="John Doe", email="john.doe@example.com")
    library_id = 1
    created_member = crud_member.create_member(db_session, member_data, library_id)
    assert created_member.name == "John Doe"
    assert created_member.email == "john.doe@example.com"
    assert created_member.library_id == 1


def test_get_member(db_session):
    member_data = schemas.MemberCreate(
        name="Jane Smith", email="jane.smith@example.com"
    )
    library_id = 1
    created_member = crud_member.create_member(db_session, member_data, library_id)
    retrieved_member = crud_member.get_member(db_session, created_member.member_id)
    assert retrieved_member
    assert retrieved_member.name == "Jane Smith"
    assert retrieved_member.email == "jane.smith@example.com"
    assert retrieved_member.library_id == 1


def test_show_member_info(db_session):
    member_data = schemas.MemberCreate(
        name="Michael Brown", email="michael.brown@example.com"
    )
    library_id = 1
    created_member = crud_member.create_member(db_session, member_data, library_id)
    shown_member = crud_member.show_member_info(db_session, created_member.member_id)
    assert shown_member
    assert shown_member.name == "Michael Brown"
    assert shown_member.email == "michael.brown@example.com"
    assert shown_member.library_id == 1


def test_remove_member(db_session):
    member_data = schemas.MemberCreate(
        name="Emma Johnson", email="emma.johnson@example.com"
    )
    library_id = 1
    created_member = crud_member.create_member(db_session, member_data, library_id)
    removed_member = crud_member.remove_member(db_session, created_member.member_id)
    assert removed_member
    assert removed_member.name == "Emma Johnson"
    assert removed_member.email == "emma.johnson@example.com"
    assert removed_member.library_id == 1
