from Scraper.Goodreads_book_scraper import book_scraper
from Scraper.Goodreads_list_scraper import list_scraper
from Class_book_record import BookRecord
from Database.SQL_uploader import update_db
from Database.SQL_classes_tables import initialise_engine_and_base
from Scraper.scrape_error import ScrapeError
from config import *
import datetime as dt
import time
import csv
import logging

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


def list_url(l_type, l_detail):
    """ Creates the URL of a Goodreads list based on system arguments.
    Defaults to most read this week in local country if none entered. """

    if l_type == "most-popular": # edit on 17/03/2021: new url format means leading zeros on month need to be removed
        return BASE_URL + "book/popular_by_date/" + str(l_detail)[:YEAR_INDEX] + "/" \
               + str(int(str(l_detail)[YEAR_INDEX:]))
    if l_type == "most-read":
        return BASE_URL + "book/most_read?category=all&country=" \
               + str(l_detail)[:COUNTRY_INDEX] + "&duration=" + str(l_detail)[-1]
    if l_type == "new-releases":
        return BASE_URL + "genres/new_releases/" + str(l_detail)
    if l_type == "custom-list":
        return BASE_URL + "list/show/" + str(l_detail)
    else:
        return BASE_URL + "book/most_read"


def scrape_books_from_list(book_id_list):
    """Take a list of Goodreads book IDs and scrape the data from the book webpages. Return a list of Book_Record
    objects that contain the scraped data."""
    book_data = []
    try:
        for book_ID in book_id_list:
            book_data_dict = book_scraper(book_ID)
            book_data.append(BookRecord(book_data_dict))
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


def web_scraper(list_type, list_detail):

    start_time = time.time()
    logger.info(f"GoodReads scraping started at {dt.datetime.now()}")

    goodreads_url = list_url(list_type, list_detail)

    engine = initialise_engine_and_base()

    try:
        book_id_list = list_scraper(goodreads_url)
    except ScrapeError:
        logger.error('Application will finish executing but will not scrape any books.')
        book_id_list = []
    except Exception as err:
        logger.error(err)
        logger.error('Application will finish executing but will not scrape any books.')
        book_id_list = []

    book_data = scrape_books_from_list(book_id_list)

    time_taken = round(time.time() - start_time, 2)
    if len(book_data) != 0:
        logger.info(f'Took {time_taken}s to scrape {len(book_data)} books,'
                    f' {round(time_taken / len(book_data), 2)}s per book.')
        try:
            update_db(book_data, goodreads_url, list_type, list_detail, engine)
        except Exception as err:
            logger.info("Writing data to CSV file")
            write_to_csv(book_data)
            logger.info(f"Data saved to file: {OUTPUT_FILE_NAME}")
            logger.error(f'Error encountered on upload to db: {err}')
