from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date, DECIMAL, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
#TODO: add to install instructions: ensure using 64bit version of python for mysqlclient install
import csv
from Class_book_record import Book_Record


SQL_LANGUAGE_CONNECTION = 'mysql://root:Logout22@localhost/mydb'
Base = declarative_base()

book_author_mapping = Table(
    "book_author_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book_records.id")),
    Column("author_id", Integer, ForeignKey("authors.id"))

)

class Book_record_dec(Base):
    __tablename__ = 'book_records'
    id = Column('id', Integer, primary_key=True)
    goodreads_id = Column('goodreads_id', Integer)
    title = Column('title', String(250))
    author = relationship('Author', secondary=book_author_mapping)
    # relationship: this will not exist as a field in the 'book_records' table, it establishes a relationship object.
    # The first arg is the table it relates to (through the mapping table)
    # secondary=book_author_mapping is the mapping table

    def __str__(self):
        return f'{self.id}, {self.goodreads_id}, {self.title}'

class Author(Base):
    __tablename__ = 'authors'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    books = relationship('Book_record_dec', secondary=book_author_mapping)

    def __str__(self):
        return f'{self.id}, {self.name}'


def get_author(author_name):
    qry = session.query(Author).filter(Author.name == author_name).all()
    if len(qry) == 0:
        author = Author()
        author.name = author_name
    else:
        author = qry[0]
    return author

if __name__ == '__main__':
    with open('20210121_book_data_b.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        test_books = [Book_Record(book) for book in reader]
    print(test_books)


    engine = create_engine(SQL_LANGUAGE_CONNECTION, echo=True)

    Base.metadata.create_all(bind=engine)
    session_maker = sessionmaker(bind=engine)

    session = session_maker()
    for book in test_books[:4]:
        record = Book_record_dec()
        record.goodreads_id = book.Book_ID
        record.title = book.Title
        author = get_author(book.Author)
        record.author = [author] # because this is one-to-many?
        session.add(record)
    session.commit()
    qry = session.query(Book_record_dec).all()
    for row in qry:
        print(row)
    qry = session.query(Author).all() # all() converts to list so we can check length
    for row in qry:
        print(row)

    session.close()


