from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import crud
from app.database import SessionLocal

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:ipekten@localhost/sample"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal.configure(bind=engine)
db = SessionLocal()

json_file_path = "C:\\Users\\yekta\\Desktop\\libmsys\\books.json"

crud.load_books_from_json(db, json_file_path)

db.close()
