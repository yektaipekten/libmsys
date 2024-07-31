import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy.orm import Session
from .models import Book
from . import models
from .actions import crud_book
import numpy as np


def get_book_data(db: Session):
    books = db.query(Book).all()
    book_data = []
    for book in books:
        book_data.append(
            {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "publication_year": book.publication_year,
                "average_rating": book.average_rating,
                "ratings_count": book.ratings_count,
                "language": book.language,
                "page_count": book.page_count,
                "description": book.description,
                "publisher": book.publisher,
                "categories": book.categories,
                "library_id": book.library_id,
            }
        )
    return pd.DataFrame(book_data)


def content_based_recommendations(book_id, book_data, top_n=5):
    tfidf = TfidfVectorizer(stop_words="english")
    book_data["description"] = book_data["description"].fillna("")
    tfidf_matrix = tfidf.fit_transform(book_data["description"])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    idx = book_data.index[book_data["book_id"] == book_id][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : top_n + 1]

    book_indices = [i[0] for i in sim_scores]
    return book_data.iloc[book_indices]


def hybrid_recommendations(member_id: int, db: Session):
    member_books = (
        db.query(models.Transaction)
        .filter(models.Transaction.member_id == member_id)
        .all()
    )

    if not member_books:
        return pd.DataFrame()

    books = db.query(models.Book).all()
    books_df = pd.DataFrame(
        [
            {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "ISBN": book.ISBN,
                "publication_year": book.publication_year,
                "average_rating": book.average_rating,
                "ratings_count": book.ratings_count,
                "language": book.language,
                "page_count": book.page_count,
                "description": book.description,
                "publisher": book.publisher,
                "categories": book.categories,
                "library_id": book.library_id,
            }
            for book in books
        ]
    )

    member_books_df = pd.DataFrame(
        [
            {
                "book_id": transaction.book.book_id,
                "title": transaction.book.title,
                "author": transaction.book.author,
                "ISBN": transaction.book.ISBN,
                "publication_year": transaction.book.publication_year,
                "average_rating": transaction.book.average_rating,
                "ratings_count": transaction.book.ratings_count,
                "language": transaction.book.language,
                "page_count": transaction.book.page_count,
                "description": transaction.book.description,
                "publisher": transaction.book.publisher,
                "categories": transaction.book.categories,
                "library_id": transaction.book.library_id,
            }
            for transaction in member_books
        ]
    )

    recommendations_df = books_df[~books_df["book_id"].isin(member_books_df["book_id"])]

    recommendations_df = recommendations_df[
        recommendations_df["categories"].isin(member_books_df["categories"])
    ]

    recommendations_df = recommendations_df.sort_values(
        by="average_rating", ascending=False
    ).head(10)

    return recommendations_df


def filtered_recommendations(category: str, language: str, title: str, db: Session):
    query = db.query(models.Book)

    if category:
        query = query.filter(models.Book.categories.like(f"%{category}%"))
    if language:
        query = query.filter(models.Book.language.like(f"%{language}%"))
    if title:
        query = query.filter(models.Book.title.like(f"%{title}%"))

    if not category and not language and not title:
        raise ValueError(
            "Enter at least one criterion (category, language, or title) to filter the books."
        )

    books = query.all()

    if not books:
        raise ValueError("No books available based on the given criteria.")

    books_df = pd.DataFrame(
        [
            {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "ISBN": book.ISBN,
                "publication_year": book.publication_year,
                "average_rating": book.average_rating,
                "ratings_count": book.ratings_count,
                "language": book.language,
                "page_count": book.page_count,
                "description": book.description,
                "publisher": book.publisher,
                "categories": book.categories,
                "library_id": book.library_id,
                "is_available": book.is_available,
            }
            for book in books
        ]
    )

    books_df = books_df.replace({np.nan: None})

    recommendations_df = books_df.sort_values(
        by="average_rating", ascending=False
    ).head(10)

    return recommendations_df.to_dict("records")


def member_recommendations(member_id: int, db: Session):
    borrowed_books = crud_book.get_borrowed_books_by_member(db, member_id)

    if not borrowed_books:
        return []

    borrowed_book_ids = [borrowed.book_id for borrowed in borrowed_books]

    books = db.query(Book).all()
    if not books:
        raise ValueError("No books available.")

    books_df = pd.DataFrame(
        [
            {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "categories": book.categories,
            }
            for book in books
        ]
    )

    books_df["combined_features"] = (
        books_df["title"].fillna("")
        + " "
        + books_df["author"].fillna("")
        + " "
        + books_df["categories"].fillna("")
    )

    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf_vectorizer.fit_transform(books_df["combined_features"])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    recommendations = []
    for book_id in borrowed_book_ids:
        book_idx = books_df.index[books_df["book_id"] == book_id].tolist()[0]
        similar_indices = cosine_similarities[book_idx].argsort()[:-11:-1]
        similar_items = [
            (books_df.iloc[i]["book_id"], cosine_similarities[book_idx][i])
            for i in similar_indices
        ]

        recommendations.extend(similar_items)

    recommendations = list(set(recommendations))
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

    recommended_books = [
        rec[0] for rec in recommendations if rec[0] not in borrowed_book_ids
    ][:10]

    return books_df[books_df["book_id"].isin(recommended_books)].to_dict("records")
