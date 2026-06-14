import logging
import mysql.connector


logger = logging.getLogger(__name__)

def get_connection():
    return mysql.connector.connect(
        host= "localhost",
        port=3309,
        user="root",
        password="root",
        database="library_db"
    )

logger.info("create the connection")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    table_1 = """CREATE TABLE IF NOT EXISTS books(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title varchar(50) NOT NULL, 
    author varchar(50) NOT NULL,
    genre ENUM("Fiction","Non-Fiction","Science","History","Other") NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    borrowed_by_member_id INT DEFAULT NULL);"""

    table_2 = """CREATE TABLE IF NOT EXISTS members(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(50) NOT NULL, 
    email varchar(50) UNIQUE NOT NULL, 
    is_active BOOLEAN NOT NULL DEFAULT FALSE, 
    total_borrows INT NOT NULL DEFAULT 0);"""

    cursor.execute(table_1)
    cursor.execute(table_2)
    conn.commit()
    cursor.close()
    conn.close()




