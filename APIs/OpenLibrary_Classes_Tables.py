"""
SQLAlchemy classes and tables for defining database and enabling upload to the database.

Author: Jordan Ribbans
"""


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import exc


openlibrary_publish_years_mapping = Table(
    "openlibrary_publish_years_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("publish_year_id", Integer, ForeignKey("openlibrary_publish_years.book_id"))
)


openlibrary_isbn_mapping = Table(
    "openlibrary_isbn_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("isbn_id", Integer, ForeignKey("openlibrary_isbn.id"))
)


openlibrary_languages_mapping = Table(
    "openlibrary_languages_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("language_id", Integer, ForeignKey("openlibrary_languages.id"))
)


openlibrary_goodreads_mapping = Table(
    "openlibrary_goodreads_mapping",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("openlibrary_book.id")),
    Column("goodreads_id", Integer, ForeignKey("openlibrary_goodreads.id"))
)


# class OpenLibraryBookInstance:
#     """
#     Class for storing OpenLibrary book data to a table
#         OL_key : str - Unique key for each book in OpenLibrary
#         Title : str
#         Author : str
#         Edition_count : int
#         Publish_years : list of strings (which are all integers)
#         ISBN : list of strings (which are all integers)
#         Languages : list of strings
#         ID_goodreads : list of strings
#
#     Author: Jordan Ribbans
#     """
#     def __init__(self, data_dict):
#         """Instantiate a Book_Record object by passing it a dict of the data required to set it's attribute values"""
#         self.Openlibrary_id = data_dict.get('key')
#         self.Title = data_dict.get('title')
#         self.Author = data_dict.get('author_name')
#         self.Edition_count = data_dict.get('edition_count')
#         self.Publish_years = data_dict.get('publish_year')
#         self.ISBN = data_dict.get('isbn')
#         self.Languages = data_dict.get('language')
#         self.ID_goodreads = data_dict.get('id_goodreads')


class OpenLibraryBook(Base):
    """Class inheriting from dectarative_base() instance Base that allows instances to be created to store the unique
    series names. Instance is initiated with below parameters taken directly from a BookRecord class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
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
    author = Column('author', String(50))
    edition_count = Column('edition_count', Integer)

    publish_years = relationship('publish_year', secondary=openlibrary_publish_years_mapping)
    isbn = relationship('ISBN', secondary=openlibrary_isbn_mapping)
    language = relationship('Language', secondary=openlibrary_languages_mapping)
    goodreads_id = relationship('Goodreads_ID', secondary=openlibrary_goodreads_mapping)

    def __init__(self, book_record_instance):
        self.openlibrary_id = book_record_instance.Openlibrary_id
        self.title = book_record_instance.Title
        self.author = book_record_instance.Author
        self.edition_count = book_record_instance.Edition_count


    def __str__(self):
        return str(self.__dict__.values())


class PublishYear(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    publish years. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        year : int

    Relationships with:
        openlibrary_book >< this class
    """
    __tablename__ = 'openlibrary_publish_years'
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer, unique=True)
    book_id = relationship('book_id', secondary=openlibrary_publish_years_mapping)

    def __init__(self, year):
        self.year = int(year)


class Language(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    languages. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        language : str

    Relationships with:
        openlibrary_book >< this class
    """
    __tablename__ = 'openlibrary_languages'
    id = Column('id', Integer, primary_key=True)
    language = Column('language', String(10), unique=True)
    book_id = relationship('book_id', secondary=openlibrary_languages_mapping)

    def __init__(self, language):
        self.language = language


class ISBN(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    ISBNs. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        isbn : str

    Relationships with:
        openlibrary_book >< this class
    """
    __tablename__ = 'openlibrary_isbn'
    id = Column('id', Integer, primary_key=True)
    isbn = Column('isbn', Integer, unique=True)
    book_id = relationship('book_id', secondary=openlibrary_isbn_mapping)

    def __init__(self, isbn):
        self.isbn = isbn


class GoodreadsID(Base):
    """Class inheriting from declarative_base() instance Base that allows instances to be created to store the unique
    GoodRead IDs. Instance is initiated with below parameters taken directly from a OpenLibraryBookInstance class instance.
    id is created sequentially as primary key.
    Parameters:
        id : int - primary key in database table
        year : int

    Relationships with:
        openlibrary_book >< this class
    """
    __tablename__ = 'openlibrary_goodreads'
    id = Column('id', Integer, primary_key=True)
    goodreads_id = Column('goodreads_id', Integer, unique=True)
    book_id = relationship('book_id', secondary=openlibrary_goodreads_mapping)

    def __init__(self, year):
        self.year = int(year)


