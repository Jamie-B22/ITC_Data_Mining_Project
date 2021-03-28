"""
Functions to implement the functionality for each option the user can give to the argparser

Author: Jamie Bamforth
"""

from config import *
from APIs.Class_NYTimes_List import NYTimesBookList
from SQL_uploader import NYT_API_update_db
from SQL_classes_tables import initialise_engine_and_base
import logging
import time
import sys

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)




def NYT_API_update_all(date):
    """Takes a date (accepts string format "YYYY-MM-DD" or "current") and fetches every NYT bestseller list for that
    date and uploads them to the database."""
    logger.debug('Initialising engine.')
    engine = initialise_engine_and_base() #TODO: this is currently created in main. Create in main and pass here, or create here?
    logger.debug('Getting NYT Bestseller encoded list names.')
    encoded_list_names = NYTimesBookList.get_list_names_encoded(NYT_API_KEY)

    for num, list_name in enumerate(encoded_list_names):
        logger.info(f'Processing list {list_name}')
        logger.debug(f'Fetching NYT Bestseller list {list_name} from API and uploading to db.')
        book_list = NYTimesBookList(list_name, date, NYT_API_KEY)
        NYT_API_update_db(book_list, engine)
        logger.debug(f'{list_name} uploaded to db.')
        time.sleep(ANTI_THROTTLE_DELAY_S)
        if num%9 == 0:
            time.sleep(60) # needs more wait time for some reason
    logger.info('Success: NYT bestseller lists uploaded to database.')


def NYT_API_update_list(list_date_detail):
    """Takes a list and a date as a combined string format [encoded-list-name],[date] (accepts date format "YYYY-MM-DD"
    or "current") and fetches the NYT bestseller list for that date and uploads it to the database."""
    logger.debug('Initialising engine.')
    engine = initialise_engine_and_base()  # TODO: this is currently created in main. Create in main and pass here, or create here?
    logger.debug('Getting NYT Bestseller list from API.')
    list_name, date = list_date_detail.split(',')
    logger.debug(f'Fetching NYT Bestseller list {list_date_detail} from API and uploading to db.')
    book_list = NYTimesBookList(list_name, date, NYT_API_KEY)
    NYT_API_update_db(book_list, engine)
    logger.info(f'Success: {list_date_detail} uploaded to db.')


def NYT_bestesller_list_names():
    """Prints to stdout the possible list names you can give to the argpaser."""
    logger.debug('Getting and printing to stdout the NYT Bestseller encoded list names.')
    encoded_list_names = NYTimesBookList.get_list_names_encoded(NYT_API_KEY)
    print('NYT bestseller list names (encoded in format that can be passed to this program):')
    for num, name in enumerate(encoded_list_names):
        print(f'{num}. "{name}"')
    print('---end of list names---')




if __name__ == '__main__':
    # some tests to check it runs as expected and logging to help debug

    formatter = logging.Formatter(
        '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('main.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


    # print(NYTimesBookList('hardcover-graphic-books', 'current', NYT_API_KEY))
    NYT_bestesller_list_names()
    NYT_API_update_list('hardcover-fiction,2019-03-04')
    NYT_API_update_all('current')