"""
Functions and SQLAlchemy enabling upload to the database.

Author: Jamie Bamforth
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
import logging
from Database.SQL_classes_tables import Author, Series, Genre, Description, Edition, List, BookUpdate,\
    NYTBestsellerList, NYTBestsellerISBN, OpenLibraryBook, PublishYear, OLISBN, Language, GoodreadsID


"""Setup Logger"""
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)



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


def get_isbn13(isbn13, session):
    """Checks if the isbn associated with isbn13 exists in the db already. If exists, returns that NYTBestsellerISBN
     object, if not creates and returns a new one."""
    qry = session.query(NYTBestsellerISBN).filter(NYTBestsellerISBN.isbn == isbn13).all()
    if len(qry) == 0:
        isbn = NYTBestsellerISBN(isbn13)
    else:
        isbn = qry[0]
    return isbn

def get_edition_from_isbn(isbn, session):
    """Checks if the edition associated with the isbn exists in the db already. If exists, returns that Edition
     object, if not returns None"""
    qry = session.query(Edition).filter(Edition.isbn == isbn).all()
    if len(qry) == 0:
        return None
    else:
        return qry[0]


def get_NYT_list(book_list, session):
    """Checks if the list associated with isbn13 exists in the db already. If exists, returns that NYTBestsellerList
     object, if not creates and returns a new one."""
    qry = session.query(NYTBestsellerList).filter(NYTBestsellerList.list_name_encoded == book_list.list_name_encoded,
                                                  NYTBestsellerList.date == book_list.date).all()
    if len(qry) == 0:
        list = NYTBestsellerList(book_list)
    else:
        list = qry[0]
    return list


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

def isbn_relationships_creator_and_adder(isbn, session):
    isbn_instance = get_isbn13(isbn, session)
    edition = get_edition_from_isbn(isbn, session)
    if edition is not None:
        isbn_instance.editions += [edition]
    session.add(isbn_instance)
    return isbn_instance

def NYT_list_relationships_creater_and_adder(isbn_instances, book_list, session):
    NYT_list = get_NYT_list(book_list, session)
    NYT_list.nyt_bestseller_isbns += isbn_instances
    session.add(NYT_list)

def initialise_session(engine):
    """Intitalise SQLAlchemy engine and session to allow uploading of records to the db. Returns the sessionmaker().
    If a connection cannot be made with the database, raise an error that will be handled in main.py to upload the book
    details to a backup csv."""
    try:
        session_maker = sessionmaker(bind=engine)
        logger.debug(f'Database connection session initialised.')
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
    logger.info(f'Attempting to upload {len(books)} books to database.')
    session = initialise_session(engine)
    create_and_commit_data(books, list_url, list_type, list_details, session)
    session.close()
    logger.debug(f'Database connection session closed.')


def NYT_list_create_and_commit_data(book_list, session):
    isbn_instances = [isbn_relationships_creator_and_adder(isbn, session) for isbn in set(book_list.get_isbn13s()
                                                                                          + book_list.get_isbn10s())]
    NYT_list_relationships_creater_and_adder(isbn_instances, book_list, session)
    session.commit()
    logger.info(f'{len(book_list.get_isbn13s())} isbns and corresponding list committed to database.')


def NYT_API_update_db(book_list, engine):
    logger.info(f'Attempting to upload {len(book_list.get_isbn13s())} NYT bestseller isbns to database.')
    session = initialise_session(engine)
    NYT_list_create_and_commit_data(book_list, session)
    session.close()
    logger.debug(f'Database connection session closed.')


# ############# Open Library Books ###############

def get_OpenLibraryBook(OL_book, session):
    qry = session.query(OpenLibraryBook).filter(OpenLibraryBook.openlibrary_id == OL_book.Openlibrary_id).all()
    if len(qry) == 0:
        book = OpenLibraryBook(OL_book)
    else:
        book = qry[0]
    return book

def get_publishyear(year, session):
    qry = session.query(PublishYear).filter(PublishYear.year == year).all()
    if len(qry) == 0:
        year = PublishYear(year)
    else:
        year = qry[0]
    return year


def get_publishyear_collection(years, session):
    return [get_publishyear(year, session) for year in set(years)]


def get_olisbn(isbn, session):
    qry = session.query(OLISBN).filter(OLISBN.isbn == isbn).all()
    if len(qry) == 0:
        isbn = OLISBN(isbn)
    else:
        isbn = qry[0]
    return isbn


def get_olisbn_collection(isbns, session):
    return [get_olisbn(isbn, session) for isbn in set(isbns)]


def get_language(language, session):
    qry = session.query(Language).filter(Language.language == language).all()
    if len(qry) == 0:
        lang = Language(language)
    else:
        lang = qry[0]
    return lang


def get_language_collection(languages, session):
    return [get_language(language, session) for language in set(languages)]


def get_goodreads_id(goodreads_id, session):
    qry = session.query(GoodreadsID).filter(GoodreadsID.goodreads_id == goodreads_id).all()
    if len(qry) == 0:
        id = GoodreadsID(goodreads_id)
    else:
        id = qry[0]
    return id


def get_goodreads_id_collection(goodreads_ids, session):
    return [get_goodreads_id(goodreads_id, session) for goodreads_id in set(goodreads_ids)]


def book_and_relationships_creator_and_adder(OL_book, session):
    book = get_OpenLibraryBook(OL_book, session)
    publishyear_collection = get_publishyear_collection(OL_book.Publish_years, session)
    book.publish_years += publishyear_collection
    isbn_collection = get_olisbn_collection(OL_book.ISBN, session)
    book.isbns += isbn_collection
    language_collection = get_language_collection(OL_book.Languages, session)
    book.languages += language_collection
    goodreads_id_collection = get_goodreads_id_collection(OL_book.ID_goodreads, session)
    book.goodreads_ids += goodreads_id_collection
    # TODO: link to goodreads
    session.add(book)



def OL_book_create_and_commit_data(OL_book, session):
    book_and_relationships_creator_and_adder(OL_book, session)
    session.commit()
    logger.info(f'Open Library book ISBN {OL_book.ISBN} committed to database.')



def OL_API_update_db(OL_book, engine):
    logger.info(f'Attempting to upload Open Library book ISBN {OL_book.ISBN} to database.')
    session = initialise_session(engine)
    OL_book_create_and_commit_data(OL_book, session)
    session.close()
    logger.debug(f'Database connection session closed.')


if __name__ == '__main__':
    # for initial testing only, will only run properly on a computer with the test csv.
    # with open('20210121_book_data_b.csv', 'r', newline='') as file:
    #     reader = csv.DictReader(file)
    #     test_books = [BookRecord(book) for book in reader]
    # print(test_books)
    # scraped_list_url = 'https://www.goodreads.com/book/most_read'
    # type_arg = 'test_type'
    # details_arg = 'test_details'
    # update_db(test_books, scraped_list_url, type_arg, details_arg, initialise_engine_and_base())
    pass
