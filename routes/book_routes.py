from fastapi import APIRouter
from database.book_db import Book

router_in_book = APIRouter()

instance = Book()


@router_in_book.post("")
def create_book(data:dict):
    return instance.create(data)

