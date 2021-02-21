from Goodreads_book_scraper import book_scraper
from Goodreads_list_scraper import list_scraper
from Class_book_record import Book_Record
import time
import csv
import sys


OUTPUT_FILE_NAME = 'test_book_data.csv'
BASE_URL = "https://www.goodreads.com/"
TYPE_ARG = 1
DETAILS_ARG = 2
YEAR_INDEX = 4
COUNTRY_INDEX = 2
TYPE = ""
DETAILS = ""

def list_url():
    """ Creates the URL of a Goodreads list based on system arguments.
    Defaults to most read this week in local country if none entered. """
    # TODO: Before next checkpoint add in choices and help statements as in command calculator exercise
    # TODO: Before next checkpoint add in errors for incorrectly entered arguments
    if len(sys.argv) == 3:
        # <type in [most-popular, most-read, new-releases, custom-list]>
        # <details in [YYYYMM, COUNTRYperiod(eg ILm), genre, customID]>
        type = sys.argv[TYPE_ARG]
        details = sys.argv[DETAILS_ARG]
    else:
        type = TYPE
        details = DETAILS
    if type == "most-popular":
        return BASE_URL + "book/popular_by_date/" + str(details)[:YEAR_INDEX] + "/" + str(details)[YEAR_INDEX:]
    if type == "most-read":
        return BASE_URL + "book/most_read?category=all&country=" + str(details)[:COUNTRY_INDEX] + "&duration=" + str(details)[-1]
    if type == "new-releases":
        return BASE_URL + "genres/new_releases/" + str(details)
    if type == "custom-list":
        return BASE_URL + "list/show/" + str(details)
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
            print(book_data[-1].__dict__)
    except ConnectionError as err:
        print(f'Failure to scrape book. {err}')
    return book_data


def write_to_csv(book_data):
    """Take a list of Book_Record objects and save each Book_record as a row in a CSV."""
    print(f'Saving scraped data in {OUTPUT_FILE_NAME}.')
    keys = book_data[0].__dict__.keys()
    with open(OUTPUT_FILE_NAME, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for book in range(len(book_data)):
            dict_writer.writerow(book_data[book].__dict__)
    print(f'Saved scraped data in {OUTPUT_FILE_NAME}.')


def main():
    """Scrape the given Goodreads list for the book IDs, then scrape each book in the list for it's data. Save that
    data as a CSV."""
    start_time = time.time()

    # book_ID_list = list_scraper('http://www.goodreads.com/book/popular_by_date/2020/11')

    goodreads_url = list_url()
    book_ID_list = list_scraper(goodreads_url)

    book_data = scrape_books_from_list(book_ID_list)

    time_taken = round(time.time() - start_time, 2)
    if len(book_data) != 0:
        print(f'Took {time_taken}s to scrape {len(book_data)} books, {round(time_taken/len(book_data),2)}s per book.')
        write_to_csv(book_data)


if __name__ == '__main__':
    main()
