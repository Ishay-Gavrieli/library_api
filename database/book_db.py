from database.db_connection import get_connection
import logging
from fastapi import HTTPException
from database.member_db import Members

instance_member = Members()

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
            logger.info("the book created successfuly")
            return {"message":"the book created successfuly"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to create book: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()


    def get_all_books(self):
        try:
            logger.info("try to get all books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books;")
            result = cursor.fetchall()
            logger.info("success to get all books")
            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get all books: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def get_book_by_id(self,id:int):
        try:
            logger.info("try to get book by id")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
            result = cursor.fetchone()
            logger.info("success to get book by id")
            return result if result else None
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get book by id: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()


    def update_book(self,id:int, data:dict):
        try:
            logger.info("try to update book")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE books SET title = %s, author = %s, genre = %s, is_available = %s , borrowed_by_member_id = %s WHERE id = %s "
            cursor.execute(sql,(data["title"],data["author"],data["genre"],data["is_available"],data["borrowed_by_member_id"],id))
            conn.commit()
            logger.info("success to update book")
            return {"message":"the book update successfuly"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to update book: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()


    def set_available(self,id,member_id,val):
        if not val:
            try:
                logger.info("try to return book")
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)

                cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
                book = cursor.fetchone()
                if not book:
                     raise HTTPException(status_code=404, detail="The book not found")
                if book["is_available"]:
                    raise HTTPException(status_code=404, detail="The book not borrowed")
                
                cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
                member = cursor.fetchone()
                if not member:
                    raise HTTPException(status_code=404, detail="The member not found")
                

                cursor.execute("SELECT borrowed_by_member_id FROM books WHERE borrowed_by_member_id = %s and id = %s", (member_id,id))
                if not cursor.fetchone():
                    raise HTTPException(status_code=400, detail="The book is not borrowed by this member")


                cursor.execute("UPDATE books SET is_available = True , borrowed_by_member_id = NULL WHERE id = %s",(id,))
                conn.commit()
                logger.info("the book return successfuly")
                return {"message":"the book return successfuly"}
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Failed to return book: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")
            finally:
                cursor.close()
                conn.close()

        try:
            logger.info("Attempting to borrow book")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT count(*) as total FROM books WHERE borrowed_by_member_id = %s", (member_id,))
            count_result = cursor.fetchone()
            if count_result["total"] >= 3:
                raise HTTPException(status_code=400, detail="Member reached maximum borrows")
            
            cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
            book = cursor.fetchone()
            if not book:
                raise HTTPException(status_code=400, detail="The book not found")

            cursor.execute("SELECT is_available FROM books WHERE id = %s", (id,))
            book = cursor.fetchone()
            if not book or not book["is_available"]:
                raise HTTPException(status_code=400, detail="The book is not available")
            
            cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
            member = cursor.fetchone()
            if not member:
                raise HTTPException(status_code=404, detail="The member not found")

            cursor.execute("SELECT is_active FROM members WHERE id = %s", (member_id,))
            member = cursor.fetchone()
            if not member or not member["is_active"]:
                raise HTTPException(status_code=400, detail="The member is not active")

            cursor.execute("UPDATE books SET is_available = False, borrowed_by_member_id = %s WHERE id = %s", (member_id, id))
            instance_member.increment_borrows(member_id)
            
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

    
    def count_total_books(self):
        try:
            logger.info("try to calculate total books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM books")
            result = cursor.fetchone()
            logger.info("success to calculate total books")
            return result["total"] 
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to calculate total books: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def count_available_books(self):
        try:
            logger.info("try to count available books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as available FROM books WHERE is_available=True")
            result = cursor.fetchone()
            logger.info("success to count available books")
            return result["available"] 
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to count available books: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def count_borrowed_books(self):
        try:
            logger.info("try to count borrowed books")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) borrows FROM books WHERE is_available=False")
            result = cursor.fetchone()
            logger.info("success to count borrowed books")
            return result["borrows"] 
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to count borrowed books: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()



    def count_by_genre(self,genre):
        try:
            logger.info("try to count by genre")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as genre FROM books where genre = %s",(genre,))
            result = cursor.fetchone()
            logger.info("success to count by genre")
            return {"Genre": genre, "COUNT": result["genre"]}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to count by genre: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def count_active_borrows_by_member(self,member_id:int):
        try:
            logger.info("try to count active borrows by member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM books where  borrowed_by_member_id = %s",(member_id,))
            result = cursor.fetchone()
            logger.info("success to count active borrows by member")
            return result["total"]
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to count active borrows by member: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()