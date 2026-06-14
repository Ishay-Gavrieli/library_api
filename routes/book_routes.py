from fastapi import APIRouter
from database.book_db import Book


router_in_book = APIRouter()

instance = Book()



@router_in_book.post("")
def create_book(data:dict):
    return instance.create(data)



@router_in_book.get("")
def all_books():
    return instance.get_all_books()


@router_in_book.get("/{id}")
def book_by_id(id:int):
    return instance.get_book_by_id(id)


@router_in_book.put("/{id}")
def update_book(id, data:dict):
    return instance.update_book(id,data)


@router_in_book.put("/{id}/return/{member_id}")
def return_book(id:int,member_id):
    return instance.set_available(id,member_id,val=False)




@router_in_book.put("/{id}/borrow/{member_id}")
def boorow_book_by_member(id:int,member_id:int):
    return instance.set_available(id,member_id,val=True)




@router_in_book.get("/borrow/{member_id}")
def count_active_borrow_book(member_id:int):
    return instance.count_active_borrows_by_member(member_id)


