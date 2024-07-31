import openai
from dotenv import load_dotenv
import os
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory

from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from sqlalchemy.orm import Session
from app.models import Book, Transaction
import logging

load_dotenv()

langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
if langchain_api_key is None:
    raise ValueError("LANGCHAIN_API_KEY environment variable is not set")

os.environ["OPENAI_API_KEY"] = openai_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_books_from_db(db: Session):
    logging.info("Loading books from database")
    books = db.query(Book).all()
    logging.info(f"Loaded {len(books)} books from database")
    return [book.title for book in books]


def create_embeddings(book_titles, batch_size=2):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectors = []
    for i in range(0, len(book_titles), batch_size):
        batch = book_titles[i : i + batch_size]
        logging.info(
            f"Processing batch {i // batch_size + 1}/{len(book_titles) // batch_size + 1}"
        )
        batch_vectors = embeddings.embed_documents(batch)
        vectors.extend(batch_vectors)
    return vectors, embeddings


def create_faiss_index(vectors, embeddings, book_titles):
    faiss_index = FAISS.from_embeddings(
        embedding=embeddings, text_embeddings=vectors, texts=book_titles
    )
    return faiss_index


class CustomRetriever:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def retrieve(self, query):
        return self.vectorstore.similarity_search(query)


def create_rag_model(db: Session):
    book_titles = load_books_from_db(db)
    vectors, embeddings = create_embeddings(book_titles)
    faiss_index = create_faiss_index(vectors, embeddings, book_titles)
    retriever = CustomRetriever(vectorstore=faiss_index)
    llm = OpenAI(model_name="text-davinci-003", api_key=openai_api_key)
    chain = ConversationBufferMemory(llm=llm, retriever=retriever)
    return chain


def get_recommendations_for_member(member_id: int, db: Session):
    logger.info("Creating RAG model")
    chain = create_rag_model(db)
    logger.info(f"Fetching transactions for Member ID: {member_id}")
    transactions = (
        db.query(Transaction).filter(Transaction.member_id == member_id).all()
    )
    read_books = [trans.book.title for trans in transactions]
    logger.info(f"Read books: {read_books}")
    query = (
        "Based on the books I have read: "
        + ", ".join(read_books)
        + ", can you recommend me some books?"
    )
    response = chain.run(query)
    logger.info(f"Recommendation response: {response}")
    return response


def get_recommendations_based_on_prompt(prompt: str, db: Session):
    chain = create_rag_model(db)
    response = chain.run(prompt)
    return response
