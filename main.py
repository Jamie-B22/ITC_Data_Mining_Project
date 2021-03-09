from Goodreads_book_scraper import book_scraper
from Goodreads_list_scraper import list_scraper
from Class_book_record import Book_Record
from SQL_uploader import update_db
from config import *
import datetime as dt
import time
import csv
import argparse
import logging
import sys

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter('%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

# create a file handler and add it to logger
file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def args_dict():
    """
    Creates a dictionary for the command line arguments
    The first parameter is the list type, and the second parameter are the list details
    """
    type_list = ['most-popular', 'most-read', 'new-releases', 'custom-list']
    detail_list = ['YYYYMM', 'COUNTRYperiod(eg ILm)', 'genre', 'customID']

    parser = argparse.ArgumentParser()
    parser.add_argument('list_type', choices=type_list, help=f"The type of list to scrape: {type_list}")
    parser.add_argument('list_detail', help=f"The details for the corresponding list type: {detail_list}")

    logger.debug("Parsing command line arguments")
    args = parser.parse_args()

    if len(vars(args)) == 2:
        l_type = args.list_type
        l_details = args.list_detail
        logger.debug("List type and detail given")
    else:
        logger.warning("Incorrect parameters given, using default list, 'most read'")
        l_type = ""
        l_details = ""

    type_detail = {"list_type": l_type, "list_detail": l_details}

    return type_detail


def list_url(l_type, l_detail):
    """ Creates the URL of a Goodreads list based on system arguments.
    Defaults to most read this week in local country if none entered. """
    # TODO: Before next checkpoint add in choices and help statements as in command calculator exercise
    # TODO: Before next checkpoint add in errors for incorrectly entered arguments

    if l_type == "most-popular":
        return BASE_URL + "book/popular_by_date/" + str(l_detail)[:YEAR_INDEX] + "/" + str(l_detail)[YEAR_INDEX:]
    if l_type == "most-read":
        return BASE_URL + "book/most_read?category=all&country=" + str(l_detail)[:COUNTRY_INDEX] + "&duration=" + str(l_detail)[-1]
    if l_type == "new-releases":
        return BASE_URL + "genres/new_releases/" + str(l_detail)
    if l_type == "custom-list":
        return BASE_URL + "list/show/" + str(l_detail)
    else:
        return BASE_URL + "book/most_read"


def scrape_books_from_list(book_ID_list):
    """Take a list of Goodreads book IDs and scrape the data from the book webpages. Return a list of Book_Record
    objects that contain the scraped data."""
    book_data = []
    try:
        for book_ID in book_ID_list:
            book_data_dict = book_scraper(book_ID)
            book_data.append(Book_Record(book_data_dict))
            # print(book_data[-1].__dict__)
    except ConnectionError as err:
        logger.error(f'Failure to scrape book. {err}')
    return book_data


def write_to_csv(book_data):
    """Take a list of Book_Record objects and save each Book_record as a row in a CSV."""
    logger.debug(f'Saving scraped data in {OUTPUT_FILE_NAME}.')
    keys = book_data[0].__dict__.keys()
    with open(OUTPUT_FILE_NAME, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for book in range(len(book_data)):
            dict_writer.writerow(book_data[book].__dict__)
    logger.info(f'Saved scraped data in {OUTPUT_FILE_NAME}.')


def main():
    """Scrape the given Goodreads list for the book IDs, then scrape each book in the list for its data. Save that
    data as a CSV."""
    start_time = time.time()
    logger.info(f"Program started at {dt.datetime.now()}")

    # book_ID_list = list_scraper('http://www.goodreads.com/book/popular_by_date/2020/11')

    command_dict = args_dict()
    list_type = command_dict["list_type"]
    list_detail = command_dict["list_detail"]
    goodreads_url = list_url(list_type, list_detail)

    book_ID_list = list_scraper(goodreads_url)

    book_data = scrape_books_from_list(book_ID_list)

    time_taken = round(time.time() - start_time, 2)
    if len(book_data) != 0:
        logger.info(f'Took {time_taken}s to scrape {len(book_data)} books, {round(time_taken/len(book_data),2)}s per book.')
        # write_to_csv(book_data)
        update_db(book_data, goodreads_url, list_type, list_detail)


if __name__ == '__main__':
    main()
