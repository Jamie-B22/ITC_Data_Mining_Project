"""
SQLAlchemy classes and tables for defining database and enabling upload to the database.

Author: Jamie Bamforth
"""


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import exc
import stdiomask
import logging


"""Setup connection to database."""
USER = input('MySQL Username:')
# masks password when run from terminal (will not mask when run in python console)
PASSWORD = stdiomask.getpass('MySQL Password:', mask='*')
SQL_LANGUAGE_CONNECTION = f'mysql://{USER}:{PASSWORD}@localhost/goodreads_data'
Base = declarative_base()


"""Setup Logger"""
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)



def initialise_engine_and_base():
    """Check credentials are correct and database exists before scraping starts. If correct and exist, return the engine
    if not raise error to be passed to main.py to communicate to user. If there is another error, log this and return
    None to allow backup to csv after scraping."""
    try:
        engine = create_engine(SQL_LANGUAGE_CONNECTION, echo=False)
        Base.metadata.create_all(bind=engine)
        return engine
    except exc.OperationalError as engine_err:
        engine_error_code = int(engine_err.args[0].split()[1].split(',')[0][1:])
        if engine_error_code == 1049:
            logger.error(f'{engine_err}. Unable to create database engine due to unknown database.')
            raise engine_err
        elif engine_error_code == 1045:
            logger.error(f'{engine_err}. Unable to create database engine due to incorrect credentials.')
            raise engine_err
        else:
            logger.error(f'{engine_err}. Unable to create database engine, data will be stored in backup csv.')
            return None

# Define mappings
edition_author_mapping = Table(
    "edition_author_mapping",
    Base.metadata,
    Column("edition_id", Integer, ForeignKey("editions.id")),
    Column("author_id", Integer, ForeignKey("authors.id"))

)

edition_series_mapping = Table(
    "edition_series_mapping",
    Base.metadata,
    Column("edition_id", Integer, ForeignKey("editions.id")),
    Column("series_id", Integer, ForeignKey("series.id"))

)

edition_genre_mapping = Table(
    "edition_genre_mapping",
    Base.metadata,
    Column("edition_id", Integer, ForeignKey("editions.id")),
    Column("genre_id", Integer, ForeignKey("genres.id"))
)

update_list_mapping = Table(
    "update_list_mapping",
    Base.metadata,
    Column("book_update_id", Integer, ForeignKey("book_updates.id")),
    Column("list_id", Integer, ForeignKey("lists.id"))
)

update_description_mapping = Table(
    "update_description_mapping",
    Base.metadata,
    Column("book_update_id", Integer, ForeignKey("book_updates.id")),
    Column("description_id", Integer, ForeignKey("descriptions.id"))
)

update_edition_mapping = Table(
    "update_edition_mapping",
    Base.metadata,
    Column("book_update_id", Integer, ForeignKey("book_updates.id")),
    Column("edition_id", Integer, ForeignKey("editions.id"))
)

edition_nyt_bestseller_mapping = Table(
    "edition_nyt_bestseller_mapping",
    Base.metadata,
    Column("edition_id", Integer, ForeignKey("editions.id")),
    Column("nyt_bestseller_isbn", String(13), ForeignKey("nyt_bestseller_isbns.isbn"))
)


nyt_bestseller_isbn_list_mapping = Table(
    "nyt_bestseller_isbn_list_mapping",
    Base.metadata,
    Column("nyt_bestseller_lists_id", Integer, ForeignKey("nyt_bestseller_lists.id")),
    Column("nyt_bestseller_isbn", String(13), ForeignKey("nyt_bestseller_isbns.isbn"))
)


class BookUpdate(Base):
    """Class inheriting from dectarative_base() instance Base that allows instances to be created to store the updates
    to a book edition with each scrape. Instance is initiated with below parameters taken directly from a BookRecord
    class instance. id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        rating : decimal to 2 d.p. and 3 s.f. - range 0-5 stars
        qty_ratings : int
        qty_reviews : int
        scrape_datetime : datetime

    Relationships with:
        Edition < this class
        Description < this class
        List < this class
    """
    __tablename__ = 'book_updates'
    id = Column('id', Integer, primary_key=True)
    rating = Column('rating', DECIMAL(3, 2))
    qty_ratings = Column('qty_ratings', Integer)
    qty_reviews = Column('qty_reviews', Integer)
    scrape_datetime = Column('scrape_datetime', String(25))

    edition = relationship('Edition', secondary=update_edition_mapping)
    description = relationship('Description', secondary=update_description_mapping)
    list = relationship('List', secondary=update_list_mapping)

    def __init__(self, book_record_instance):
        self.rating = book_record_instance.Rating
        self.qty_ratings = book_record_instance.Qty_ratings
        self.qty_reviews = book_record_instance.Qty_reviews
        self.scrape_datetime = book_record_instance.Scrape_datetime

    def __str__(self):
        return str(self.__dict__.values())


class Author(Base):
    """Class inheriting from dectarative_base() instance Base that allows instances to be created to store the unique
    author names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        name : str

    Relationships with:
        Edition > this class
    """
    __tablename__ = 'authors'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    editions = relationship('Edition', secondary=edition_author_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


class Series(Base):
    """Class inheriting from dectarative_base() instance Base that allows instances to be created to store the unique
    series names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        name : str

    Relationships with:
        Edition > this class
    """
    __tablename__ = 'series'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    editions = relationship('Edition', secondary=edition_series_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


class Genre(Base):
    """Class inheriting from dectarative_base() instance Base that allows instances to be created to store the unique
    genre names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        name : str

    Relationships with:
        Edition >< this class
    """
    __tablename__ = 'genres'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    editions = relationship('Edition', secondary=edition_genre_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


class Description(Base):
    """Class inheriting from dectarative_base() instance Base that allows instances to be created to store the unique
    description strings. Separate to updates as each string is quite long and only changes occasionally, so can be
    re-used between updates. Instance is initiated with below parameters taken directly from a BookRecord class instance
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        description : str

    Relationships with:
        BookUpdate > this class
    """
    __tablename__ = 'descriptions'
    id = Column('id', Integer, primary_key=True)
    description = Column('description', String(10000))  # TODO:deal with error string is too long (truncate str[:10000])
    book_updates = relationship('BookUpdate', secondary=update_description_mapping)

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return f'{self.id}, {self.description}'


class List(Base):
    """Class inheriting from dectarative_base() instance Base that allows List instances to be created to store the
    unique list information. Instance is initiated with url, type and detail parameters determined from the user input
    in main.py.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        type : str
        details : str
        url : str

    Relationships with:
        BookUpdate > this class
    """
    __tablename__ = 'lists'
    id = Column('id', Integer, primary_key=True)
    type = Column('type', String(250))
    details = Column('details', String(250))
    url = Column('url', String(500), unique=True)
    book_updates = relationship('BookUpdate', secondary=update_list_mapping)

    def __init__(self, list_url, list_type, list_details):
        self.type = list_type
        self.details = list_details
        self.url = list_url

    def __str__(self):
        return f'{self.id}, {self.type}, {self.details}, {self.url}'


class Edition(Base):
    """Class inheriting from dectarative_base() instance Base that allows instances to be created to store the unique
    series names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        goodreads_id : str
        title : str
        format : str
        number_in_series : str
        release_date : date
        first_published_date : date
        qty_pages : int

    Relationships with:
        BookUpdate > this class
        Author < this class
        Series < this class
        Genre >< this class
    """
    __tablename__ = 'editions'
    id = Column('id', Integer, primary_key=True)
    goodreads_id = Column('goodreads_id', Integer)
    isbn = Column('isbn', String(13))
    title = Column('title', String(250))
    format = Column('format', String(250))
    number_in_series = Column('number_in_series', String(250))
    # earlier and some Linux versions of MySQL have issue with passing a string to a date here,
    # so keep as string of length 10.
    release_date = Column('release_date', String(10))
    first_published_date = Column('first_published_date', String(10))
    qty_pages = Column('qty_rpages', Integer)

    book_updates = relationship('BookUpdate', secondary=update_edition_mapping)
    author = relationship('Author', secondary=edition_author_mapping)
    # relationship: this will not exist as a field in the 'editions' table, it establishes a relationship object.
    # The first arg is the table it relates to (through the mapping table)
    # secondary=book_author_mapping is the mapping table
    series = relationship('Series', secondary=edition_series_mapping)
    genres = relationship('Genre', secondary=edition_genre_mapping)
    nyt_bestsellers_isbns = relationship('NYTBestsellerISBN', secondary=edition_nyt_bestseller_mapping)


    def __init__(self, book_record_instance):
        self.goodreads_id = book_record_instance.Book_ID
        self.isbn = book_record_instance.ISBN
        self.title = book_record_instance.Title  # .encode('UTF-16', errors='replace')
        self.format = book_record_instance.Format
        self.number_in_series = book_record_instance.Number_in_series
        self.release_date = book_record_instance.Release_date
        self.first_published_date = book_record_instance.First_published_date
        self.qty_pages = book_record_instance.Qty_pages

    def __str__(self):
        return str(self.__dict__.values())

class NYTBestsellerISBN(Base):

    __tablename__ = 'nyt_bestseller_isbns'
    isbn = Column('isbn', String(13), primary_key=True)

    editions = relationship('Edition', secondary=edition_nyt_bestseller_mapping)
    nyt_bestseller_lists = relationship('NYTBestsellerList', secondary=nyt_bestseller_isbn_list_mapping)

    def __init__(self, isbn):
        self.isbn = isbn

    def __str__(self):
        return str(self.__dict__.values())


class NYTBestsellerList(Base):

    __tablename__ = 'nyt_bestseller_lists'
    id = Column('id', Integer, primary_key=True)
    list_name_encoded = Column('list_name_encoded', String(250))
    date = Column('date', String(10))

    nyt_bestseller_isbns = relationship('NYTBestsellerISBN', secondary=nyt_bestseller_isbn_list_mapping)

    def __init__(self, NYTimesBookList):
        self.list_name_encoded = NYTimesBookList.list_name_encoded
        self.date = NYTimesBookList.date

    def __str__(self):
        return str(self.__dict__.values())




def create_tables():
    """If database is empty or incomplete, ensures all tables are created according to the definitions in the classes
    and tables in this file (SWL_classes_tables.py)"""
    engine = create_engine(SQL_LANGUAGE_CONNECTION, echo=True)
    Base.metadata.create_all(bind=engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    session.close()

if __name__ == '__main__':
    create_tables()
