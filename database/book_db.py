from database.db_connection import get_connection


class Book:
    def create(self,data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "INSERT INTO books (title,author,genre,is_available,borrowed_by_number_id) values (%s,%s,%s,True,NULL)"
        cursor.execute(sql,(data["title"],data["author"],data["genre"]))
        conn.commit()
        cursor.close()
        conn.close()



