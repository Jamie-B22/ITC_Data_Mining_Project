"""
Functions and SQLAlchemy classes for defining database and enabling upload to the database.

Author: Jamie Bamforth
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import exc
import csv
import stdiomask
import logging
import sys
from Class_book_record import BookRecord


"""Setup connection to database."""
USER = input('MySQL Username:')
# masks password when run from terminal (will not mask when run in python console)
PASSWORD = stdiomask.getpass('MySQL Password:', mask='*')  
SQL_LANGUAGE_CONNECTION = f'mysql://{USER}:{PASSWORD}@localhost/goodreads_data'
Base = declarative_base()


"""Setup Logger"""
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

# create a file handler and add it to logger
file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


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


class BookUpdate(Base):
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
    __tablename__ = 'authors'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    editions = relationship('Edition', secondary=edition_author_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


class Series(Base):
    __tablename__ = 'series'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    editions = relationship('Edition', secondary=edition_series_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


class Genre(Base):
    __tablename__ = 'genres'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True)
    editions = relationship('Edition', secondary=edition_genre_mapping)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.id}, {self.name}'


class Description(Base):
    __tablename__ = 'descriptions'
    id = Column('id', Integer, primary_key=True)
    description = Column('description', String(10000))  # TODO:deal with error string is too long (truncate str[:10000])
    book_updates = relationship('BookUpdate', secondary=update_description_mapping)

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return f'{self.id}, {self.description}'


class List(Base):
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
    __tablename__ = 'editions'
    id = Column('id', Integer, primary_key=True)
    goodreads_id = Column('goodreads_id', Integer)
    title = Column('title', String(250))
    format = Column('format', String(250))
    number_in_series = Column('number_in_series', String(250))
    release_date = Column('release_date', Date)
    first_published_date = Column('first_published_date', Date)
    qty_pages = Column('qty_rpages', Integer)

    book_updates = relationship('BookUpdate', secondary=update_edition_mapping)
    author = relationship('Author', secondary=edition_author_mapping)
    # relationship: this will not exist as a field in the 'editions' table, it establishes a relationship object.
    # The first arg is the table it relates to (through the mapping table)
    # secondary=book_author_mapping is the mapping table
    series = relationship('Series', secondary=edition_series_mapping)
    genres = relationship('Genre', secondary=edition_genre_mapping)

    def __init__(self, book_record_instance):
        self.goodreads_id = book_record_instance.Book_ID
        self.title = book_record_instance.Title  # .encode('UTF-16', errors='replace')
        self.format = book_record_instance.Format
        self.number_in_series = book_record_instance.Number_in_series
        self.release_date = book_record_instance.Release_date
        self.first_published_date = book_record_instance.First_published_date
        self.qty_pages = book_record_instance.Qty_pages

    def __str__(self):
        return str(self.__dict__.values())


# =============== Functions are below this line, SQLAlchemy classes and tables above ===============
# all get functions are intended to check if the object already exists in the database, returning the existing object if
# exists, a new one if it doesn't.

def get_author(author_name, session):
    """Checks if an author of author_name exists in the db already. If exists, returns that author object, if not
    creates and returns a new one."""
    qry = session.query(Author).filter(Author.name == author_name).all()
    if len(qry) == 0:
        author = Author(author_name)
    else:
        author = qry[0]
    return author


def get_series(series_name, session):
    """Checks if series of series_name exists in the db already. If exists, returns that series object, if not
    creates and returns a new one."""
    qry = session.query(Series).filter(Series.name == series_name).all()
    if len(qry) == 0:
        series = Series(series_name)
    else:
        series = qry[0]
    return series


def get_genre(genre_name, session):
    """Checks if a genre of genre_name exists in the db already. If exists, returns that genre object, if not
    creates and returns a new one."""
    qry = session.query(Genre).filter(Genre.name == genre_name).all()
    if len(qry) == 0:
        genre = Genre(genre_name)
    else:
        genre = qry[0]
    return genre


def get_genre_collection(genres, session):
    """Takes list of genre strings and returns a list of the appropriate Genre instances."""
    return [get_genre(genre, session) for genre in genres]


def get_description(description_text, session):
    """Checks if a description of description_text exists in the db already. If exists, returns that description object,
    if not creates and returns a new one."""
    qry = session.query(Description).filter(Description.description == description_text).all()
    if len(qry) == 0:
        description = Description(description_text)
    else:
        description = qry[0]
    return description


def get_edition(book_record_instance, session):
    """Checks if the edition of book_record_instance exists in the db already. If exists, returns that edition object,
    if not creates and returns a new one."""
    qry = session.query(Edition).filter(Edition.goodreads_id == book_record_instance.Book_ID and
                                        Edition.title == book_record_instance.Title and
                                        Edition.format == book_record_instance.Format).all()
    if len(qry) == 0:
        edition = Edition(book_record_instance)
    else:
        edition = qry[0]
    return edition


def get_book_list(list_url, list_type, list_details, session):
    """Checks if a the list associated with list_url exists in the db already. If exists, returns that list object, if
    not creates and returns a new one."""
    qry = session.query(List).filter(List.url == list_url).all()
    if len(qry) == 0:
        book_list = List(list_url, list_type, list_details)
    else:
        book_list = qry[0]
    return book_list


def ensure_set(obj):
    """Takes an object and returns that object as a set if the ibject is a set or the JSON string encoding of a set,
    else returns None. The use case for this is when extracting sets that have been uploaded to csv and converting them
    back to a set object."""
    if isinstance(obj, str):
        return {elem for elem in obj.strip("{'|'}").split("', '")}
    elif isinstance(obj, set):
        return obj
    else:
        return None


def book_and_relationships_creator_and_adder(book_record_instance, session):
    """Takes book_record_instance and uses its parameters to create a new or update an existing Edition, BookUpdate,
    Author, Series, Genre and Descrition objects. It then adds the relevant relationships btween objects adding the
    relationships to the BookUpdate (book_updates) objects. Returns the BookUpdate instance."""
    # TODO: split into instance creator and relationships creator?
    record = BookUpdate(book_record_instance)
    edition = get_edition(book_record_instance, session)
    record.edition = [edition]
    author = get_author(book_record_instance.Author, session)
    edition.author = [author]  # because this is one-to-many?
    if book_record_instance.Series is not None:  # don't create a series relationship if series doesn't exist
        series = get_series(book_record_instance.Series, session)
        edition.series = [series]
    book_record_instance.Genres = ensure_set(book_record_instance.Genres)
    genres_collection = get_genre_collection(book_record_instance.Genres, session)
    edition.genres = genres_collection
    description = get_description(book_record_instance.Description, session)
    # TODO: log if this was successful and add a debug level with issues.
    # TODO: put somewhere that description only exists as a separate table is to save memory,
    #  each description is associated with multiple book title pulls.
    record.description = [description]
    session.add(record)
    return record


def list_and_relationships_creator_and_adder(list_url, list_type, list_details, book_updates, session):
    """Takes list information (list_url, list_type, list_details) and creates a new or updates an existing List object,
    adding the relationships to the BookUpdate (book_updates) objects. Returns the List instance."""
    book_list = get_book_list(list_url, list_type, list_details, session)
    book_list.book_updates += book_updates  # updates appends to mapping table for that list rather than overwriting
    session.add(book_list)
    return book_list


def initialise_session(engine):
    """Intitalise SQLAlchemy engine and session to allow uploading of records to the db. Returns the sessionmaker().
    If a connection cannot be made with the database, raise an error that will be handled in main.py to upload the book
    details to a backup csv."""
    try:
        session_maker = sessionmaker(bind=engine)
        return session_maker()
    except exc.SQLAlchemyError as session_err:
        logger.error(f'{session_err}. Unable to initialise connection to database, data not saved in database.')
        raise session_err


def create_and_commit_data(books, list_url, list_type, list_details, session):
    """Takes book and list details and calls functions that creates individual book records and a list record in the db
    and their relationships."""
    book_updates = [book_and_relationships_creator_and_adder(book, session) for book in books]
    list_and_relationships_creator_and_adder(list_url, list_type, list_details, book_updates, session)
    session.commit()
    logger.info(f'{len(book_updates)} books committed to database.')


def update_db(books, list_url, list_type, list_details, engine):
    """Take a list of book record instances (books) and the Goodreads list details in which the books were found in
    (list_url, list_type, list_details), create a database session and upload these to the database."""
    logger.info(f'Uploading {len(books)} books to database.')
    session = initialise_session(engine)
    logger.debug(f'Database connection session initialised.')
    create_and_commit_data(books, list_url, list_type, list_details, session)
    session.close()
    logger.debug(f'Database connection session closed.')


if __name__ == '__main__':
    # for initial testing only, will only run properly on a computer with the test csv.
    with open('20210121_book_data_b.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        test_books = [BookRecord(book) for book in reader]
    print(test_books)
    scraped_list_url = 'https://www.goodreads.com/book/most_read'
    type_arg = 'test_type'
    details_arg = 'test_details'
    update_db(test_books, scraped_list_url, type_arg, details_arg, initialise_engine_and_base())
