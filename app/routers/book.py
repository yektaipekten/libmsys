from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Book as SQLAlchemyBook
from app.schemas import Book as PydanticBook, BookCreate
from app.database import get_db_session
from app.actions import crud_book as crud
import requests

router = APIRouter()

GOOGLE_BOOKS_API_KEY = "AIzaSyCOcRzJFfkcyaoet-Uw1ZuVqKUb3ll_xYc"


@router.get("/{book_id}/availability", response_model=PydanticBook)
async def check_availability(book_id: int, db: Session = Depends(get_db_session)):
    db_book = crud.check_availability(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "book_id": db_book.book_id,
        "title": db_book.title,
        "author": db_book.author,
        "ISBN": db_book.ISBN,
        "publication_year": db_book.publication_year,
        "library_id": db_book.library_id,
        "is_available": db_book.is_available,
        "average_rating": db_book.average_rating,
        "ratings_count": db_book.ratings_count,
        "language": db_book.language,
        "page_count": db_book.page_count,
        "description": db_book.description,
        "publisher": db_book.publisher,
        "categories": db_book.categories,
    }


@router.post("/{book_id}/return")
async def return_book(book_id: int, db: Session = Depends(get_db_session)):
    db_book = crud.return_book_availability(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "message": f"The book '{db_book.title}' with ID {db_book.book_id} has been returned."
    }


@router.get("/search/{title}", response_model=list[PydanticBook])
async def search_book(title: str, db: Session = Depends(get_db_session)):
    inserted_books = []
    total_books_to_fetch = 10000
    books_per_request = 40

    for start_index in range(0, total_books_to_fetch, books_per_request):
        url = f"https://www.googleapis.com/books/v1/volumes?q={title}&key={GOOGLE_BOOKS_API_KEY}&startIndex={start_index}&maxResults={books_per_request}"
        response = requests.get(url)

        if response.status_code == 200:
            books = response.json().get("items", [])
            if not books:
                break

            for item in books:
                book_data = item.get("volumeInfo", {})

                try:
                    publication_date = book_data.get("publishedDate", "N/A")
                    publication_year = (
                        int(publication_date.split("-")[0])
                        if publication_date != "N/A"
                        and publication_date.split("-")[0].isdigit()
                        else None
                    )

                    book = BookCreate(
                        title=book_data.get("title", "N/A"),
                        author=(
                            ", ".join(book_data.get("authors", []))
                            if "authors" in book_data
                            else None
                        ),
                        ISBN=(
                            book_data.get("industryIdentifiers", [{}])[0].get(
                                "identifier", "N/A"
                            )
                            if "industryIdentifiers" in book_data
                            else "N/A"
                        ),
                        publication_year=publication_year,
                        library_id=1,
                        is_available=True,
                        average_rating=book_data.get("averageRating", None),
                        ratings_count=book_data.get("ratingsCount", None),
                        language=book_data.get("language", None),
                        page_count=book_data.get("pageCount", None),
                        description=book_data.get("description", None),
                        publisher=book_data.get("publisher", None),
                        categories=(
                            ", ".join(book_data.get("categories", []))
                            if "categories" in book_data
                            else None
                        ),
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=500, detail=f"Error parsing book data: {e}"
                    )

                try:
                    db_book = crud.insert_book(db, book)
                    inserted_books.append(db_book)
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error inserting book into database: {e}",
                    )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error fetching data from Google Books API",
            )

    return inserted_books


@router.get("/all", response_model=list[PydanticBook])
async def get_all_books(db: Session = Depends(get_db_session)):
    db_books = crud.get_all_books(db)
    return db_books
