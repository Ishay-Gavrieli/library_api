import logging
from fastapi import HTTPException
from database.db_connection import get_connection


logger = logging.getLogger(__name__)

class Members:
    def create(self,data:dict):
        try:
            logger.info("try to create member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "INSERT INTO members (name,email,is_active) values (%s,%s,True)"
            cursor.execute(sql,(data["name"],data["email"]))
            conn.commit()
            logger.info("the member created successfuly")
            return {"message":"the member created successfuly"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to borrow book: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def get_all_members(self):
        try:
            logger.info("try to get all members")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members;")
            result = cursor.fetchall()
            logger.info("success to get all members")
            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to borrow book: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def get_member_by_id(self,id:int):
        try:
            logger.info("try to get member by id")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members WHERE id = %s",(id,))
            result = cursor.fetchone()
            logger.info("success to get member by id")
            return result if result else None
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get member by id: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def update_member(self,id:int, data:dict):
        try:
            logger.info("try to update member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "UPDATE members SET name = %s, email = %s,is_active = %s , total_borrows = %s WHERE id = %s "
            cursor.execute(sql,(data["name"],data["email"],data["is_active"],data["total_borrows"],id))
            conn.commit()
            logger.info("success to update member")
            return {"message":"the member update successfuly"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to update member: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def deactivate_member(self,id:int):
        try:
            logger.info("try to update deactivate member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE members SET is_active = false WHERE id = %s",(id,))
            conn.commit()
            logger.info("success to update deactivate member")
            return {"message":"the member update successfuly"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to update deactivate member: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()


    def activate_member(self,id:int):
        try:
            logger.info("try to update activate member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE members SET is_active = True WHERE id = %s",(id,))
            conn.commit()
            logger.info("success to update activate member")
            return {"message":"the member update successfuly"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to update activate member: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def count_active_members(self):
        try:
            logger.info("try to count activate member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as active FROM members WHERE is_active = True")
            result = cursor.fetchone()
            logger.info("success to count activate member")
            return result["active"]
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to count activate member: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            conn.close()

    def get_top_member(self):
        try:
            logger.info("try to return the top borrows member")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1")
            result = cursor.fetchall()
            logger.info("success to return the top borrows member")
            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to return the top borrows member:{e}")
            raise HTTPException(status_code=500,detail="Internal server error")
        finally:
            cursor.close()
            conn.close()


