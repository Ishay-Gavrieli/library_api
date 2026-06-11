# plan for the project

## 1. 
A library data management system that is responsible for creating books, updating books, borrowing and returning them to the member.
the actions: creating library members, updating them, deactivating and activating them, and it can return data about the users and the books. 


## 2.
docker: docker run --name  mysql-library_db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=library_db -p 3309:3306 -d mysql:latest

docker:docker exec -it mysql-library_db mysql -u root -p


## 3.
library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db_connection.py  
│   │   ├── book_db.py  
│   │   └── member_db.py  
│   ├── routes/  
│   │   ├── book_routes.py  
│   │   ├── member_routes.py  
│   │   └── report_routes.py  
│   └── logs/
|       ├── basic_logger.py
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore


## 4.
# books table:
id INT PRIMARY KEY AUTO_INCREMENT
title varchar(50) NOT NULL 
author varchar(50) NOT NULL
genre ENUM("Fiction","Non-Fiction","Science","History","Other") NOT NULL
available_is BOOLEAN NOT NULL DEFAULT TRUE
id_member_by_borrowed DEFAULT NULL 


# members table:
id INT PRIMARY KEY AUTO_INCREMENT
name varchar(50) NOT NULL 
email UNIQUE NOT NULL 
is_active NOT NULL DEFAULT FALSE 
borrows_total INT NOT NULL



## 5.
# System rules:
1. When creating a book, the user sends genre/author/title and the function should update
is_available=True, borrowed_by=NULL

2. When updating and creating a book, the genre must have the value we set in the enum, any other value will return a 404 error

3. When creating a friend, the user sends mail/name and the function must add total_borrows=0 is_active=True

4. The email must be unique and if it already exists, it returns a 422 error

5. When borrowing a book if the friend does not exist (False=active_is) the book cannot be borrowed 

6. It is not possible to borrow a book that is already borrowed if the parameter is_available=false

7. A friend cannot have more than three books

8. A book can only be returned if I borrowed it


## 6. רשימת endpoints
# Method | Endpoint | Description
POST /books : create book
books/ GET : all books
GET /books/{id} : book by ID
PATCH /books/{id} : update book
PATCH /books/{id}/borrow/{member_id} : Lending a book to a member
PATCH /books/{id}/return/{member_id} : Returning a book to a member
POST /members : create member
GET /members : all members
GET /members/{id} : member by ID 
PATCH /members/{id} : update member
PATCH /members/{id}/deactivate : disable member
PATCH /members/{id}/activate : active member
GET /reports/summary : general report
GET /reports/books-by-genre :books by genre
GET /reports/top-member : the most active member


## 7.
# system flow
Http Request -> Fastapi -> Endpoint -> Query -> Database

## 8.
# commands
python -m venv venv
venv\Scripts\activate
python main.py
pip install -r requierments
(fastapi,uvicorn,mysql-connector-python)
