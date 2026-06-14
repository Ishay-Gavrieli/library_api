from fastapi import FastAPI
import uvicorn
from database import db_connection
from routes import book_routes,report_routes,member_routes

app = FastAPI()

db_connection.create_tables()


app.include_router(book_routes.router_in_book,prefix="/books",tags=["books"])


app.include_router(member_routes.router_in_member,prefix="/members",tags=["members"])


app.include_router(report_routes.router_in_report,prefix="/reports",tags=["reports"])



if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)


