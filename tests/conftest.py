import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base
from app.models import Library, Book, Member, Transaction

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:ipekten@localhost/sample"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_test_data(db_session: Session):
    library = Library(name="Test Library", address="123 Library St")
    db_session.add(library)
    db_session.commit()

    book = Book(
        title="Test Book",
        author="Author A",
        ISBN="1234567890",
        library_id=library.library_id,
        is_available=True,
    )
    db_session.add(book)
    db_session.commit()

    member = Member(
        name="John Doe", email="john.doe@example.com", library_id=library.library_id
    )
    db_session.add(member)
    db_session.commit()

    transaction = Transaction(book_id=book.book_id, member_id=member.member_id)
    db_session.add(transaction)
    db_session.commit()

    yield

    db_session.query(Transaction).delete()
    db_session.query(Book).delete()
    db_session.query(Member).delete()
    db_session.query(Library).delete()
    db_session.commit()
