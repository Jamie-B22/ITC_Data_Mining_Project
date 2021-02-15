from Goodreads_book_scraper import book_scraper
from Goodreads_list_scraper import list_scraper
from Proxy_generator import proxy_generator
from Class_book_record import Book_Record
import time
import random
import csv

ANTI_THROTTLE_DELAY = 10
OUTPUT_FILE_NAME = 'book_data.csv'

def write_to_csv(book_data):
    print(f'Saving scraped data in {OUTPUT_FILE_NAME}.')
    keys = book_data[0].__dict__.keys()
    with open(OUTPUT_FILE_NAME, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for book in range(len(book_data)):
            dict_writer.writerow(book_data[book].__dict__)
    print(f'Saved scraped data in {OUTPUT_FILE_NAME}.')


def main():
    start_time = time.time()
    # get proxy addresses to use at random to prevent throttling. Use randomly rather than as an iterator as
    # next(iterator) will eventually run out and have to be re-instantiated.
    proxy_addresses = proxy_generator()

    book_ID_list = list_scraper('http://www.goodreads.com/book/popular_by_date/2020/11', random.choice(proxy_addresses))
    book_data = []
    try:
        for book_ID in book_ID_list:
            book_data_dict = book_scraper(book_ID, random.choice(proxy_addresses))
            book_data.append(Book_Record(book_data_dict))
            print(book_data[-1].__dict__)
    except ConnectionError as err:
        print(f'Failure to scrape book. {err}')
    time_taken = round(time.time() - start_time, 2)
    if len(book_data) != 0:
        print(f'Took {time_taken}s to scrape {len(book_data)} books, {round(time_taken/len(book_data),2)}s per book.')
        write_to_csv(book_data)


if __name__ == '__main__':
    main()
