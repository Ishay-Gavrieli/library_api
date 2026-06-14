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
            logger.info("the member created successfuly")
            return {"the member created successfuly"}
        except:
            logger.error("faild to create")
            raise HTTPException(status_code=500,detail="faild to create")
        

    def get_all_members(self):
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


    def get_member_by_id(self,id:int):
        try:
            logger.info("get member by id")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members WHERE id = %s",(id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result if result else None
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")


    def update_member(self,id:int, data:dict):
        try:
            logger.info("update member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE members SET name = %s, email = %s,is_active = %s , total_borrows = %s WHERE id = %s "
            cursor.execute(sql,(data["name"],data["email"],data["is_active"],data["total_borrows"],id))
            conn.commit()
            cursor.close()
            conn.close()
            return {"the member update successfuly"}
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")
        

    def deactivate_member(self,id:int):
        try:
            logger.info("update deactivate member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE members SET is_active = false WHERE id = %s",(id,))
            conn.commit()
            cursor.close()
            conn.close()
            return {"the member update successfuly"}
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")

    def activate_member(self,id:int):
        try:
            logger.info("update activate member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE members SET is_active = True WHERE id = %s",(id,))
            conn.commit()
            cursor.close()
            conn.close()
            return {"the member update successfuly"}
        except:
            logger.error("faild")
            raise HTTPException(status_code=500,detail="faild")


    def count_active_members(self):
        try:
            logger.info("count activate member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as active FROM members WHERE is_active = True")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result["active"]
        except Exception as e:
            logger.error(f"faild {e}")
            raise HTTPException(status_code=500,detail="faild")

    def get_top_member(self):
        try:
            logger.info("return the top borrows member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e: 
            logger.error(f"faild {e}")
            raise HTTPException(status_code=500,detail="faild")
        


