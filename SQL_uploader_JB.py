from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date, DECIMAL, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
#TODO: add to install instructions: ensure using 64bit version of python for mysqlclient install
import csv
from Class_book_record import Book_Record

#TODO: does session object need to be passed to functions it is used in?
#TODO: change dates to date type
#TODO: documentation and justification on why columns are in tables at the top
password = 'Logout22' #TODO: make this user input?
SQL_LANGUAGE_CONNECTION = f'mysql://root:{password}@localhost/mydb'
Base = declarative_base() #TODO: can this be in the main fn?

book_author_mapping = Table(
    "book_author_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book_records.id")),
    Column("author_id", Integer, ForeignKey("authors.id"))

)

# book_series_mapping = Table(
#     "book_series_mapping",
#     Base.metadata,
#     Column("book_id", Integer, ForeignKey("book_records.id")),
#     Column("series_id", Integer, ForeignKey("series.id"))
#
# )
#
# book_genre_mapping = Table(
#     "book_genre_mapping",
#     Base.metadata,
#     Column("book_id", Integer, ForeignKey("book_records.id")),
#     Column("genre_id", Integer, ForeignKey("genres.id"))
# )

class Book_record_declarative(Base):
    __tablename__ = 'book_records'
    id = Column('id', Integer, primary_key=True)
    goodreads_id = Column('goodreads_id', Integer)
    title = Column('title', String(250))
    format = Column('format', String(250))
    number_in_series = Column('number_in_series', String(250))
    rating = Column('rating', DECIMAL(3,2))
    release_date = Column('release_date', String(10))
    first_published_date = Column('first_published_date', String(10))
    qty_ratings = Column('qty_ratings', Integer)
    qty_reviews = Column('qty_reviews', Integer)
    qty_pages = Column('qty_rpages', Integer)
    scrape_datetime = Column('scrape_datetime', String(25))

    author = relationship('Author', secondary=book_author_mapping)
    # relationship: this will not exist as a field in the 'book_records' table, it establishes a relationship object.
    # The first arg is the table it relates to (through the mapping table)
    # secondary=book_author_mapping is the mapping table

    def __init__(self, book_record_instance):
        self.goodreads_id = book_record_instance.Book_ID
        self.title = book_record_instance.Title
        self.format = book_record_instance.Format
        self.number_in_series = book_record_instance.Number_in_series
        self.rating = book_record_instance.Rating
        self.release_date = book_record_instance.Release_date
        self.first_published_date = book_record_instance.First_published_date
        self.qty_ratings = book_record_instance.Qty_ratings
        self.qty_reviews = book_record_instance.Qty_reviews
        self.qty_pages = book_record_instance.Qty_pages
        self.scrape_datetime = book_record_instance.Scrape_datetime

    def __str__(self):
        return str(self.__dict__.values())


class Author(Base):
    __tablename__ = 'authors'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    books = relationship('Book_record_declarative', secondary=book_author_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


def get_author(author_name):
    qry = session.query(Author).filter(Author.name == author_name).all()
    if len(qry) == 0:
        author = Author(author_name)
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
        record = Book_record_declarative(book)
        author = get_author(book.Author)
        record.author = [author] # because this is one-to-many?
        session.add(record)
    session.commit()
    qry = session.query(Book_record_declarative).all()
    for row in qry:
        print(row)
    qry = session.query(Author).all() # all() converts to list so we can check length
    for row in qry:
        print(row)

    session.close()


