from .actions import (
    crud_book,
    crud_member,
    crud_library,
    crud_transaction,
    crud_librarian,
)
from . import models, schemas
from sqlalchemy.orm import Session


# book
create_book = crud_book.create_book
get_book = crud_book.get_book
delete_book = crud_book.delete_book
check_availability = crud_book.check_availability
return_book_availability = crud_book.return_book_availability
add_book = crud_book.add_book

# member
create_member = crud_member.create_member
get_member = crud_member.get_member
show_member_info = crud_member.show_member_info
remove_member = crud_member.remove_member


def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


# library
get_library = crud_library.get_library
get_libraries = crud_library.get_libraries
create_library = crud_library.create_library

# TODO: buna gerek yok, lazım olduğu yerde ilgili yerden import edilmesi daha sağlıklı

# transaction
issue_book = crud_transaction.issue_book
return_book = crud_transaction.return_book
borrow_book = crud_transaction.borrow_book
show_borrowed_books = crud_transaction.show_borrowed_books
show_returned_books = crud_transaction.show_returned_books

# librarian
add_librarian = crud_librarian.add_librarian
remove_librarian = crud_librarian.remove_librarian
get_librarian = crud_librarian.get_librarian
update_librarian = crud_librarian.update_librarian
