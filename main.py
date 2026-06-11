from fastapi import FastAPI
import uvicorn
from database import db_connection
from routes import book_routes

app = FastAPI()

db_connection.create_tables()


app.include_router(book_routes.router_in_book,prefix="/books")

@app.get("/")
def description():
    return db_connection.new()


if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)


