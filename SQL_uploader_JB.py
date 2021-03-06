from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date, DECIMAL, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
#TODO: add to install instructions: ensure using 64bit version of python for mysqlclient install
import csv
import json
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

book_series_mapping = Table(
    "book_series_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book_records.id")),
    Column("series_id", Integer, ForeignKey("series.id"))

)

book_genre_mapping = Table(
    "book_genre_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book_records.id")),
    Column("genre_id", Integer, ForeignKey("genres.id"))
)

book_list_mapping = Table(
    "book_list_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book_records.id")),
    Column("list_id", Integer, ForeignKey("lists.id"))
)

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
    series = relationship('Series', secondary=book_series_mapping)
    genres = relationship('Genre', secondary=book_genre_mapping)
    description = relationship('Description')

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

class Series(Base):
    __tablename__ = 'series'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    books = relationship('Book_record_declarative', secondary=book_series_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


class Genre(Base):
    __tablename__ = 'genres'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    books = relationship('Book_record_declarative', secondary=book_genre_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'

class List(Base):
    __tablename__ = 'lists'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    url = Column('url', String(500), unique=True)
    books = relationship('Book_record_declarative', secondary=book_list_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}, {self.url}'


class Description(Base):
    __tablename__ = 'book_descriptions'
    id = Column('id', Integer, primary_key=True)
    book_id = Column("book_id", Integer, ForeignKey("book_records.id"))
    description = Column('description', String(7500))
    books = relationship('Book_record_declarative')

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return f'{self.id}, {self.description}'


def get_author(author_name):
    qry = session.query(Author).filter(Author.name == author_name).all()
    if len(qry) == 0:
        author = Author(author_name)
    else:
        author = qry[0]
    return author

def get_series(series_name):
    qry = session.query(Series).filter(Series.name == series_name).all()
    if len(qry) == 0:
        series = Series(series_name)
    else:
        series = qry[0]
    return series

def get_genre(genre_name):
    qry = session.query(Genre).filter(Genre.name == genre_name).all()
    if len(qry) == 0:
        genre = Genre(genre_name)
    else:
        genre = qry[0]
    return genre


def get_genre_collection(genres):
    return [get_genre(genre) for genre in genres]


def ensure_set(obj): # TODO: could return False otherwise?
    if isinstance(obj, str):
        return {elem for elem in obj.strip("{'|'}").split("', '")}
    else:
        return obj

def book_and_relationships_creator_and_adder(book_record_instance):
    record = Book_record_declarative(book_record_instance)
    author = get_author(book_record_instance.Author)
    record.author = [author]  # because this is one-to-many?
    if len(
            book_record_instance.Series) > 0:  # don't create a series relationship if series doesn't exist #TODO: change to None scraping?
        series = get_series(book_record_instance.Series)
        record.series = [series]
    book_record_instance.Genres = ensure_set(book_record_instance.Genres)
    genres_collection = get_genre_collection(book_record_instance.Genres)
    record.genres = genres_collection
    description = Description(book_record_instance.Description)
    record.description = [description]
    session.add(record)
    return record

if __name__ == '__main__':
    with open('20210121_book_data_b.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        test_books = [Book_Record(book) for book in reader]
    print(test_books)


    engine = create_engine(SQL_LANGUAGE_CONNECTION, echo=True)

    Base.metadata.create_all(bind=engine)
    session_maker = sessionmaker(bind=engine)

    session = session_maker()
    [book_and_relationships_creator_and_adder(book) for book in test_books[:4]]
    scraped_list = {'URL': 'test_URL.com', 'Book_IDs':[148623, 175351, 7396319, 36030]}
    session.commit()
    # log how many records added vs length of book list
    qry = session.query(Book_record_declarative).all()
    for row in qry:
        print(row)
    qry = session.query(Author).all() # all() converts to list so we can check length
    for row in qry:
        print(row)

    session.close()


