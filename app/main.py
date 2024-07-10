from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine, Base
from .routers import library, book, member, librarian, transaction, recommendation

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(book.router, prefix="/books", tags=["books"])
app.include_router(librarian.router, prefix="/librarians", tags=["librarians"])
app.include_router(member.router, prefix="/members", tags=["members"])
app.include_router(library.router, prefix="/libraries", tags=["libraries"])
app.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
app.include_router(
    recommendation.router, prefix="/recommendations", tags=["recommendations"]
)
