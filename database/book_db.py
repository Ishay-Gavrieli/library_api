from database.db_connection import get_connection
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class Book:
    def create(self,data:dict):
        try:
            logger.info("start createing book")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "INSERT INTO books (title,author,genre) values (%s,%s,%s)"
            cursor.execute(sql,(data["title"],data["author"],data["genre"]))
            conn.commit()
            cursor.close()
            conn.close()
            return {"the book created successfuly"}
        except:
            logger.error("faild to create")
            raise HTTPException(status_code=500,detail="faild to create")


    def get_all_books(self):
        try:
            logger.info("get all books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books;")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")


    def get_book_by_id(self,id:int):
        try:
            logger.info("get book by id")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result if result else None
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")



    def update_book(self,id:int, data:dict):
        try:
            logger.info("update book")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE books SET title = %s, author = %s, genre = %s, is_available = %s , borrowed_by_member_id = %s WHERE id = %s "
            cursor.execute(sql,(data["title"],data["author"],data["genre"],data["is_available"],data["borrowed_by_member_id"],id))
            conn.commit()
            cursor.close()
            conn.close()
            return {"the book update successfuly"}
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")


    def set_available(self,id:int, val,member_id):
        try:
            logger.info("update avalilable book")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE books SET is_available = %s , borrowed_by_member_id = %s WHERE id = %s "
            cursor.execute(sql,(val,member_id,id))
            conn.commit()
            cursor.close()
            conn.close()
            return {"the book update successfuly"}
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")

    def count_total_books(self):
        try:
            logger.info("count total books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) FROM books")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result 
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")


    def count_available_books(self):
        try:
            logger.info("count available books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available=True")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result 
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")


    def count_borrowed_books(self):
        try:
            logger.info("count borrowed books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available=False")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result 
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")
    
    def count_by_genre(self,genre):
        try:
            logger.info("count by genre")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(%s) FROM books",(genre,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result 
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")
    
    def count_active_borrows_by_member(self,member_id):
        try:
            logger.info("count active borrows by number")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books WHERE borrowed_by_member_id = %s LIMIT 3",(member_id,))
            result = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return result
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")
