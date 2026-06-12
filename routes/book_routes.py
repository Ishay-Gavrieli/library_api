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
def update_available(id:int, val,member_id):
    return instance.set_available(id,val,member_id)




@router_in_book.put("/{id}/borrow/{member_id}")
def count_active_by_member(id,member_id):
    data = instance.count_active_borrows_by_member(member_id)
    return {"id":id , "data":data}


