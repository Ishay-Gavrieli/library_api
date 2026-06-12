from fastapi import APIRouter
from database.book_db import Book


router_in_report = APIRouter()

instance = Book()

@router_in_report.get("/summary")
def count_books(condition: bool = None):
    if condition == True:
        return instance.count_available_books()
    elif condition == False:
        return instance.count_borrowed_books()

    return instance.count_total_books()


@router_in_report.get("/books-by-genre")
def count_books_by_genre(genre):
    return instance.count_by_genre(genre)