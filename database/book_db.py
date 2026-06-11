from database.db_connection import get_connection


class Book:
    def create(self,data:dict):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "INSERT INTO books (title,author,genre) values (%s,%s,%s)"
        cursor.execute(sql,(data["title"],data["author"],data["genre"]))
        conn.commit()
        cursor.close()
        conn.close()
        return {"the book created successfuly"}


    def get_all_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result



    def get_book_by_id(self,id:int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result if result else None
    

    def update_book(self,id:int, data:dict):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "UPDATE books SET title = %s, author = %s, genre = %s, is_available = %s , borrowed_by_member_id = %s WHERE id = %s "
        cursor.execute(sql,(data["title"],data["author"],data["genre"],data["is_available"],data["borrowed_by_member_id"],id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"the book update successfuly"}
    

    def set_available(self,id:int, val,member_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "UPDATE books SET is_available = %s , borrowed_by_member_id = %s WHERE id = %s "
        cursor.execute(sql,(val,member_id,id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"the book update successfuly"}
    

    def count_total_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM books")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result 
    

    def count_available_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM books WHERE is_available=True")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result 
    
    def count_borrowed_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM books WHERE is_available=False")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result 
    
    def count_by_genre(self,genre):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(%s) FROM books",(genre,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result 
    
    def count_active_borrows_by_member(self,member_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE borrowed_by_member_id = %s LIMIT 3",(member_id,))
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
