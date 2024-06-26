from fastapi import FastAPI
from .routers import book, transaction, member, librarian
from .database import engine
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(book.router)
app.include_router(transaction.router)
app.include_router(member.router)
app.include_router(librarian.router)
