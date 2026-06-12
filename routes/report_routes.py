from fastapi import APIRouter
from database.book_db import Book
from database.member_db import Members

router_in_report = APIRouter()

instance = Book()

instance_member = Members()


@router_in_report.get("/summary")
def count_books(condition: bool = None):
    if condition == True:
        data_books = instance.count_available_books()
        data_members = instance_member.count_active_members()
        return {"data_books":data_books,"data_members":data_members}
    elif condition == False:
        data_books = instance.count_borrowed_books()
        data_members = instance_member.count_active_members()
        return {"data_books":data_books,"data_members":data_members}

    data_books = instance.count_total_books()
    data_members = instance_member.count_active_members()
    return {"data_books":data_books,"data_members":data_members}


@router_in_report.get("/books-by-genre")
def count_books_by_genre(genre):
    return instance.count_by_genre(genre)


@router_in_report.get("/top-member")
def top_member():
    return instance_member.get_top_member()




