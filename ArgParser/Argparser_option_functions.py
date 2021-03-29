"""
Functions to implement the functionality for each option the user can give to the argparser

Author: Jamie Bamforth and Jordan Ribbans
"""

from config import *
from APIs.Class_NYTimes_List import NYTimesBookList
from Database.SQL_uploader import NYT_API_update_db, OL_API_update_db
from Database.SQL_classes_tables import initialise_engine_and_base
from APIs.OpenLibrary_API_Search import author_search, title_search, isbn_search, OpenLibraryBookInstance
import logging
import time
import sys

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


def NYT_API_update_all(date):
    """Takes a date (accepts string format "YYYY-MM-DD" or "current") and fetches every NYT bestseller list for that
    date and uploads them to the database."""
    logger.debug('Initialising engine.')
    engine = initialise_engine_and_base()
    logger.debug('Getting NYT Bestseller encoded list names.')
    encoded_list_names = NYTimesBookList.get_list_names_encoded(NYT_API_KEY)
    upload_count = 0
    for num, list_name in enumerate(encoded_list_names):
        logger.info(f'Processing list {list_name}')
        logger.debug(f'Fetching NYT Bestseller list {list_name} from API and uploading to db.')
        try:
            book_list = NYTimesBookList(list_name, date, NYT_API_KEY)
        except KeyError:
            logger.info(f'First request for {list_name} from API throttled, waiting 2 minutes and trying again.')
            time.sleep(120) # if first attempt is throttled, wait 2 mins and try again
            book_list = NYTimesBookList(list_name, date, NYT_API_KEY)
        try:
            NYT_API_update_db(book_list, engine)
            logger.debug(f'{list_name} uploaded to db.')
            upload_count += 1
        except Exception as err:
            logger.error(f'Unable to upload {list_name} to db due to {err}.')

        time.sleep(ANTI_THROTTLE_DELAY_S)
        if (num+1)%9 == 0:
            time.sleep(30) # needs more wait time for some reason
    logger.info(f'Success: {upload_count}/{len(encoded_list_names)} NYT bestseller lists uploaded to database.')


def NYT_API_update_list(list_date_detail):
    """Takes a list and a date as a combined string format [encoded-list-name],[date] (accepts date format "YYYY-MM-DD"
    or "current") and fetches the NYT bestseller list for that date and uploads it to the database."""
    logger.debug('Initialising engine.')
    engine = initialise_engine_and_base()
    logger.debug('Getting NYT Bestseller list from API.')
    list_name, date = list_date_detail.split(',')
    logger.debug(f'Fetching NYT Bestseller list {list_date_detail} from API and uploading to db.')
    book_list = NYTimesBookList(list_name, date, NYT_API_KEY)
    try:
        NYT_API_update_db(book_list, engine)
        logger.info(f'Success: {list_date_detail} uploaded to db.')
    except Exception as err:
        logger.error(f'Unable to upload {list_date_detail} to db due to {err}.')


def NYT_bestesller_list_names(blank_option_arg_placeholder=None):
    """Prints to stdout the possible list names you can give to the argpaser.
    blank_option_arg_placeholder is for compatibility with the way the functions are called in main"""
    logger.debug('Getting and printing to stdout the NYT Bestseller encoded list names.')
    encoded_list_names = NYTimesBookList.get_list_names_encoded(NYT_API_KEY)
    print('NYT bestseller list names (encoded in format that can be passed to this program):')
    for num, name in enumerate(encoded_list_names):
        print(f'{num}. "{name}"')
    print('---end of list names---')


def OL_API_update_by_author(author):
    """
    Takes an author name and uploads all books by this author from Open Library
    """
    logger.debug('Initialising engine.')
    engine = initialise_engine_and_base()
    logger.debug('Getting OpenLibrary books by Author')
    books = author_search(author)
    if len(books) > 0:
        for book_dict in books:
            book = OpenLibraryBookInstance(book_dict)
            try:
                OL_API_update_db(book, engine)
            except Exception as err:
                logger.error(f'Unable to upload {book.Title} to db due to {err}.')
    else:
        logger.info(f"No results returned for {author}")



def OL_API_update_by_title(title):
    """
    Takes a book title and uploads to the database all books returned from Open Library with similar titles
    """
    logger.debug('Initialising engine.')
    engine = initialise_engine_and_base()
    logger.debug('Getting OpenLibrary books by Title')
    books = title_search(title)
    if len(books) > 0:
        for book_dict in books:
            book = OpenLibraryBookInstance(book_dict)
            try:
                OL_API_update_db(book, engine)
            except Exception as err:
                logger.error(f'Unable to upload {book.Title} to db due to {err}.')
    else:
        logger.info(f"No results returned for {title}")


def OL_API_update_by_isbn(isbn):
    """
    Takes an ISBN and uploads to the database the book returned from Open Library with this ISBN
    """
    logger.debug('Initialising engine.')
    engine = initialise_engine_and_base()
    logger.debug('Getting OpenLibrary books by ISBN')
    books = isbn_search(isbn)
    if len(books) > 0:
        for book_dict in books:
            book = OpenLibraryBookInstance(book_dict)
            try:
                OL_API_update_db(book, engine)
            except Exception as err:
                logger.error(f'Unable to upload {book.Title} to db due to {err}.')
    else:
        logger.info(f"No results returned for {isbn}")



if __name__ == '__main__':
    # some tests to check it runs as expected and logging to help debug

    formatter = logging.Formatter(
        '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('../main.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


    # print(NYTimesBookList('hardcover-graphic-books', 'current', NYT_API_KEY))
    NYT_bestesller_list_names()
    NYT_API_update_list('hardcover-fiction,2019-03-04')
    NYT_API_update_all('current')