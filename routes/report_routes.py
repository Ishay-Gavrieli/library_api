from fastapi import APIRouter
from database.book_db import Book
from database.member_db import Members

router_in_report = APIRouter()

instance = Book()

instance_member = Members()


@router_in_report.get("/summary")
def count_books():
    count_available = instance.count_available_books()
    count_active = instance_member.count_active_members()
    count_borrowed = instance.count_borrowed_books()
    count_total = instance.count_total_books()
    return {"total_books": count_total,
            "available_books": count_available,
            "currently_borrowed": count_borrowed,
            "active_members": count_active}


@router_in_report.get("/books-by-genre")
def count_books_by_genre():
    return instance.count_by_genre()


@router_in_report.get("/top-member")
def top_member():
    return instance_member.get_top_member()




