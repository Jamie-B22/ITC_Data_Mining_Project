from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import csv
from Class_book_record import Book_Record


SQL_LANGUAGE_CONNECTION = 'sqlite:///:memory:'
# need to install mysqlclient. To install mysqlclient need "microsoft C++ build tools" here: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
BASE = declarative_base()

class book_record_dec(BASE):
    __tablename__ = 'book_records'
    id = Column('id', Integer, primary_key=True)
    goodreads_id = Column('goodreads_id', Integer)
    title = Column('title', String)

    def __str__(self):
        return f'{self.id}, {self.goodreads_id}, {self.title}'


if __name__ == '__main__':
    with open('20210121_book_data_b.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        test_books = [Book_Record(book) for book in reader]
    print(test_books)


    engine = create_engine(SQL_LANGUAGE_CONNECTION, echo=True)

    BASE.metadata.create_all(bind=engine)
    session_maker = sessionmaker(bind=engine)

    session = session_maker()
    for book in test_books[:4]:
        record = book_record_dec()
        record.goodreads_id = book.Book_ID
        record.title = book.Title
        session.add(record)
    session.commit()
    qry = session.query(book_record_dec).all()
    for row in qry:
        print(row)
    session.close()


