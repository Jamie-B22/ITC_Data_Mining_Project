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

nyt_bestseller_isbn_list_mapping = Table(
    "nyt_bestseller_isbn_list_mapping",
    Base.metadata,
    Column("lists_id", Integer, ForeignKey("nyt_bestseller_lists.id")),
    Column("isbn", String(13), ForeignKey("nyt_bestseller_isbns.isbn"))
)


class BookUpdate(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the updates
    to a book edition with each scrape. Instance is initiated with below parameters taken directly from a BookRecord
    class instance. id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
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
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    author names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
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
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    series names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
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
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    genre names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Kwy:
        id : int - primary key in database table
    Attributes:
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
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    description strings. Separate to updates as each string is quite long and only changes occasionally, so can be
    re-used between updates. Instance is initiated with below parameters taken directly from a BookRecord class instance
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
        description : str

    Relationships with:
        BookUpdate > this class
    """
    __tablename__ = 'descriptions'
    id = Column('id', Integer, primary_key=True)
    description = Column('description',
                         String(10000))  # TODO: deal with error string is too long (truncate str[:10000])
    book_updates = relationship('BookUpdate', secondary=update_description_mapping)

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return f'{self.id}, {self.description}'


class List(Base):
    """Class inheriting from declarative_base() instance Base that allows List instances to be created to store the
    unique list information. Instance is initiated with url, type and detail parameters determined from the user input
    in main.py.
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
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
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    series names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
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
    goodreads_id = Column('goodreads_id', String(250), ForeignKey('openlibrary_goodreads.goodreads_id'))
    isbn = Column('isbn', String(13), ForeignKey('nyt_bestseller_isbns.isbn'))
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
    nyt_bestsellers_isbns = relationship('NYTBestsellerISBN', back_populates='editions')
    ol_goodreads_id = relationship('GoodreadsID', back_populates='editions')

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
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
        ISBNs associated with books on NYT Bestsellers Lists. Instance is initiated with below parameters taken directly
        from a NYTimesBookList class instance.
        Attributes:
            isbn : str - alphanumeric code of length 10 or 13 (Primary Key)

        Relationships with:
            Editions - this class
            NYTBestsellerList >< this class
        """
    __tablename__ = 'nyt_bestseller_isbns'
    isbn = Column('isbn', String(13), primary_key=True)

    # one to one relationship were the 'back_populates' argument is the relationship object defined in 'Edition' class
    editions = relationship('Edition', uselist=False, back_populates="nyt_bestsellers_isbns")
    nyt_bestseller_lists = relationship('NYTBestsellerList', secondary=nyt_bestseller_isbn_list_mapping)

    def __init__(self, isbn):
        self.isbn = isbn

    def __str__(self):
        return str(self.__dict__.values())


class NYTBestsellerList(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
        NYT Bestsellers Lists published on a certain date. Instance is initiated with below parameters taken directly
        from a NYTimesBookList class instance.
        Key:
            id : int - primary key in database table
        Attributes:
            list_name_encoded : str
            date : str (format YYYY-MM-DD)

        Relationships with:
            NYTBestsellerISBN >< this class
        """
    __tablename__ = 'nyt_bestseller_lists'
    id = Column('id', Integer, primary_key=True)
    list_name_encoded = Column('list_name_encoded', String(250))
    date = Column('date', String(10))

    nyt_bestseller_isbns = relationship('NYTBestsellerISBN', secondary=nyt_bestseller_isbn_list_mapping)

    def __init__(self, nytimesbooklist):
        self.list_name_encoded = nytimesbooklist.list_name_encoded
        self.date = nytimesbooklist.date

    def __str__(self):
        return str(self.__dict__.values())


# ############ Open Library API #################

openlibrary_publish_years_mapping = Table(
    "openlibrary_publish_years_mapping",
    Base.metadata,
    Column("open_library_book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("publish_year_id", Integer, ForeignKey("openlibrary_publish_years.id"))
)

openlibrary_isbn_mapping = Table(
    "openlibrary_isbn_mapping",
    Base.metadata,
    Column("open_library_book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("isbn", String(13), ForeignKey("openlibrary_isbn.isbn"))
)

openlibrary_languages_mapping = Table(
    "openlibrary_languages_mapping",
    Base.metadata,
    Column("open_library_book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("language_id", Integer, ForeignKey("openlibrary_languages.id"))
)

openlibrary_goodreads_mapping = Table(
    "openlibrary_goodreads_mapping",
    Base.metadata,
    Column("open_library_book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("goodreads_id", String(250), ForeignKey("openlibrary_goodreads.goodreads_id"))
)


class OpenLibraryBook(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    series names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
        openlibrary_id : str
        title : str
        author : str
        edition_count : str

    Relationships with:
        Publish_years > this class
        ISBN > this class
        Language > this class
        Goodreads_ID > this class
    """
    __tablename__ = 'openlibrary_book'
    id = Column('id', Integer, primary_key=True)
    openlibrary_id = Column('openlibrary_id', String(50))
    title = Column('title', String(250))
    author = Column('author', String(250))
    edition_count = Column('edition_count', Integer)

    publish_years = relationship('PublishYear', secondary=openlibrary_publish_years_mapping)
    isbns = relationship('OLISBN', secondary=openlibrary_isbn_mapping)
    languages = relationship('Language', secondary=openlibrary_languages_mapping)
    goodreads_ids = relationship('GoodreadsID', secondary=openlibrary_goodreads_mapping)

    def __init__(self, book_record_instance):
        self.openlibrary_id = book_record_instance.Openlibrary_id
        self.title = book_record_instance.Title
        self.author = book_record_instance.Author
        self.edition_count = book_record_instance.Edition_count

    def __str__(self):
        return str(self.__dict__.values())


class PublishYear(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    publish years. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class
    instance.
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
        year : int

    Relationships with:
        openlibrary_book >< this class
    """
    __tablename__ = 'openlibrary_publish_years'
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer)

    OLbooks = relationship('OpenLibraryBook', secondary=openlibrary_publish_years_mapping)

    def __init__(self, year):
        self.year = int(year)


class OLISBN(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    ISBNs. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class instance.
    id is created sequentially as primary key.
    Attributes:
        isbn : str - alphanumeric code of length 10 or 13 (Primary Key)

    Relationships with:
        openlibrary_book >< this class
    """
    __tablename__ = 'openlibrary_isbn'
    isbn = Column('isbn', String(13), primary_key=True)

    OLbook = relationship('OpenLibraryBook', secondary=openlibrary_isbn_mapping)

    def __init__(self, isbn):
        self.isbn = isbn


class Language(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    languages. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class instance.
    id is created sequentially as primary key.
    Key:
        id : int - primary key in database table
    Attributes:
        language : str

    Relationships with:
        openlibrary_book >< this class
    """
    __tablename__ = 'openlibrary_languages'
    id = Column('id', Integer, primary_key=True)
    language = Column('language', String(10))

    book_id = relationship('OpenLibraryBook', secondary=openlibrary_languages_mapping)

    def __init__(self, language):
        self.language = language


class GoodreadsID(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    GoodRead IDs. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class
    instance.
    id is created sequentially as primary key.
    Attributes:
        goodreads_id : string   (Primary Key)

    Relationships with:
        openlibrary_book >< this class
        Edition - this class
    """
    __tablename__ = 'openlibrary_goodreads'
    goodreads_id = Column('goodreads_id', String(250), primary_key=True)

    OLbook = relationship('OpenLibraryBook', secondary=openlibrary_goodreads_mapping)
    editions = relationship('Edition', uselist=False, back_populates="ol_goodreads_id")

    def __init__(self, goodreads_id):
        self.goodreads_id = goodreads_id


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
