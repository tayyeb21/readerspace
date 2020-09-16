import os
import csv
# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Sequence
# from sqlalchemy.dialects.postgresql import TEXT
# metadata = MetaData()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

# engine   = create_engine("postgres://postgres:root@localhost/readerspace", echo=True)
# print(os.getenv("DATABASE_URL"))
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
engine = create_engine(os.getenv("DATABASE_URL"),echo=True)
db     = scoped_session(sessionmaker(bind=engine))
""" 
users = Table('users', metadata,
            Column('id',Integer,Sequence('users_id_seq'), primary_key=True),
            Column('firstname',String(20) , nullable=False),
            Column('middlename',String(20) , nullable=True),
            Column('lastname',String(20) , nullable=False),
            Column('email',String(120) , nullable=False),
            Column('password',String(24), nullable=False)
)
books = Table('books',metadata,
            Column('id',Integer,Sequence('books_id_seq'), primary_key=True),
            Column('title' ,String(50),nullable=False),
            Column('isbn',String(20),nullable=False),
            Column('year',Integer, nullable=False),
            Column('authorname',String(50),nullable=False)
)
userReview = Table('userReview',metadata,
                Column('id',Integer,Sequence('userReview_id_seq'), auto_increment=True, primary_key=True),
                Column('user_Id', None, ForeignKey('users.id')),
                Column('book_Id', None, ForeignKey('books.id')),
                Column('ratings',Integer, nullable=False),
                Column('review',TEXT,nullable=True)
                )
metadata.create_all(engine)
 """
def createTable():
    db.execute("""CREATE TABLE users (
            id Serial NOT NULL,
            firstname VARCHAR(20) NOT NULL,
            middlename VARCHAR(20),
            lastname VARCHAR(20) NOT NULL,
            email VARCHAR(120) NOT NULL,
            password VARCHAR(24) NOT NULL,
            PRIMARY KEY (id)
    )""")
    db.execute(""" CREATE TABLE books (
            id Serial NOT NULL,
            title VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            isbn VARCHAR(20) NOT NULL,
            year INTEGER NOT NULL,
            authorname VARCHAR(50) NOT NULL,
            PRIMARY KEY (id)
    )""")
    db.execute("""CREATE TABLE "userreview" (
            id Serial NOT NULL,
            "user_id" INTEGER,
            "book_id" INTEGER,
            ratings INTEGER NOT NULL,
            review TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY("user_id") REFERENCES users (id),
            FOREIGN KEY("book_id") REFERENCES books (id)
    )""")
def main():
    # res = db.execute( "CREATE TABLE book(bookId SERIAL PRIMARY KEY, bookTitle varchar(50), bookISBN varchar(25), authorId int, bookYear int)" )
    books = open("books.csv")
    buffer = csv.reader(books)
    description = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Eos ut, recusandae accusamus sed natus exercitationem blanditiis debitis ipsam asperiores delectus obcaecati numquam commodi laboriosam pariatur, nam enim molestias architecto necessitatibus.";
    next(buffer)
    # for isbn, title, description, author, year in buffer:
    for isbn, title, author, year in buffer:
        year = int(float(year))
        # print(type(year))   
        db.execute("INSERT INTO books (title,description,isbn,year,authorname) VALUES (:title, :desc, :isbn, :year, :author)",
                    {"title": title, "desc":description, "isbn": isbn, "year": year, "author": author})

    rows = db.execute("Select * from books").fetchall()
    for row in rows:
        print(f"Records added: Title: {row.title} ISBN: {row.isbn} Year: {row.year} Author: {row.authorname}")
        # print(res)
        # print(f"Records added: Title: {title} ISBN: {isbn} Year: {year} Author: {author}")
    # db.commit()

def fetch():
    rows = db.execute("SELECT * FROM books").fetchall()
    print(type(rows))
    print(f"rows = {rows}")
    for row in rows:
        print(f"Id: {row.id} Title: {row.title} ISBN: {row.isbn} Year: {row.year} Author: {row.authorname}")


# print("hello")/

if __name__ == "__main__":
    createTable()
    main()
    # fetch()
    db.commit()