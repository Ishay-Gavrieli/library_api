import logging
from fastapi import HTTPException
from database.db_connection import get_connection


logger = logging.getLogger(__name__)

class Members:
    def create(self,data:dict):
        try:
            logger.info("start createing member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "INSERT INTO members (name,email,is_active) values (%s,%s,True)"
            cursor.execute(sql,(data["name"],data["email"]))
            conn.commit()
            cursor.close()
            conn.close()
            return {"the member created successfuly"}
        except:
            logger.error("faild to create")
            raise HTTPException(status_code=500,detail="faild to create")
        

    def get_all_members():
        try:
            logger.info("get all members")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members;")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")



