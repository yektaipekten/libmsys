from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class Library(Base):
    __tablename__ = "libraries"

    library_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))

    books = relationship("Book", back_populates="library")
    members = relationship("Member", back_populates="library")
    librarians = relationship("Librarian", back_populates="library")


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    ISBN = Column(String(255), index=True)
    publication_year = Column(Integer)
    library_id = Column(Integer, ForeignKey("libraries.library_id"))
    is_available = Column(Boolean, default=True)
    average_rating = Column(Float, nullable=True)
    ratings_count = Column(Integer, nullable=True)
    language = Column(String(255), nullable=True)
    page_count = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    publisher = Column(String(255), nullable=True)
    categories = Column(String(255), nullable=True)

    library = relationship("Library", back_populates="books")
    transactions = relationship("Transaction", back_populates="book")
    borrowed_books = relationship("BorrowedBook", back_populates="book")


class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
    phone_number = Column(String(255))
    library_id = Column(Integer, ForeignKey("libraries.library_id"))

    library = relationship("Library", back_populates="members")
    transactions = relationship("Transaction", back_populates="member")
    borrowed_books = relationship("BorrowedBook", back_populates="member")


class Librarian(Base):
    __tablename__ = "librarians"

    librarian_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
    phone_number = Column(String(255))
    library_id = Column(Integer, ForeignKey("libraries.library_id"))

    library = relationship("Library", back_populates="librarians")


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    member_id = Column(Integer, ForeignKey("members.member_id"))
    action = Column(String(255), nullable=False)
    issue_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="transactions")
    member = relationship("Member", back_populates="transactions")


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.member_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))
    borrowed_date = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowed_books")
