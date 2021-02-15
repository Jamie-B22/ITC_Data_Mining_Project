from Goodreads_book_scraper import book_scraper
from Goodreads_list_scraper import list_scraper
from Class_book_record import Book_Record
import time
import csv


OUTPUT_FILE_NAME = 'book_data.csv'


def scrape_books_from_list(book_id_list):
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


def write_to_csv(book_data):
    """Take a list of Book_Record objects and save each Book_record as a row in a CSV."""
    print(f'Saving scraped data in {OUTPUT_FILE_NAME}.')
    keys = book_data[0].__dict__.keys()
    with open(OUTPUT_FILE_NAME, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for book in range(len(book_data)):
            dict_writer.writerow(book_data[book].__dict__)
    print(f'Saved scraped data in {OUTPUT_FILE_NAME}.')


def main():
    """Scrape the given Goodreads list for the book IDs, then scrape each book in the list for it's data. Save that
    data as a CSV."""
    start_time = time.time()

    book_ID_list = list_scraper('http://www.goodreads.com/book/popular_by_date/2020/11')
    book_data = scrape_books_from_list(book_ID_list)

    time_taken = round(time.time() - start_time, 2)
    if len(book_data) != 0:
        print(f'Took {time_taken}s to scrape {len(book_data)} books, {round(time_taken/len(book_data),2)}s per book.')
        write_to_csv(book_data)


if __name__ == '__main__':
    main()
