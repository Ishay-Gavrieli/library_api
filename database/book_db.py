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
            logger.info("the book created successfuly")
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


    def return_book(self,id:int):
        try:
            logger.info("return book")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE books SET is_available = True , borrowed_by_member_id =NULL WHERE id = %s",(id,))
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("the book return successfuly")
            return {"the book return successfuly"}
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
    
    def borrow_book(self, id: int, member_id: int):
        try:
            logger.info("Attempting to borrow book")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT count(*) as total FROM books WHERE borrowed_by_member_id = %s", (member_id,))
            count_result = cursor.fetchone()
            if count_result["total"] >= 3:
                raise HTTPException(status_code=400, detail="Member reached maximum borrows")

            cursor.execute("SELECT is_available FROM books WHERE id = %s", (id,))
            book = cursor.fetchone()
            if not book or not book['is_available']:
                raise HTTPException(status_code=400, detail="The book is not available")

            cursor.execute("SELECT is_active FROM members WHERE id = %s", (member_id,))
            member = cursor.fetchone()
            if not member or not member["is_active"]:
                raise HTTPException(status_code=400, detail="The member is not active")

            cursor.execute("UPDATE books SET is_available = False, borrowed_by_member_id = %s WHERE id = %s", (member_id, id))
            cursor.execute("UPDATE members SET total_borrows = total_borrows + 1 WHERE id = %s", (member_id,))
            
            conn.commit()
            logger.info("The book borrowed successfully")
            return {"message": "The book borrowed successfully"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to borrow book: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
            
        finally:
            cursor.close()
            conn.close()