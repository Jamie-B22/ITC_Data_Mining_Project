from Goodreads_book_scraper import book_scraper
from Goodreads_list_scraper import list_scraper
from Proxy_generator import proxy_generator
import time
import random
import csv

def main():
    start_time = time.time()
    # get proxy addresses to use at random to prevent throttling. Use randomly rather than as an iterator as
    # next(iterator) will eventually run out and have to be re-instantiated.
    proxy_addresses = proxy_generator() # TODO: add exception handling for if one proxy is dead?
    book_ID_list = list_scraper('https://www.goodreads.com/book/popular_by_date/2020/11', random.choice(proxy_addresses))
    book_data = [book_scraper(book_ID, random.choice(proxy_addresses)) for book_ID in book_ID_list[:3]] # TODO: fails on too many requests? add a wait time?
    print(book_data)
    time_taken = round(time.time() - start_time, 2)
    print(f'Took {time_taken}s to scrape {len(book_data)} books, {round(time_taken/len(book_data),2)}s per book.')

    keys = book_data[0].keys()
    with open('book_data.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(book_data)


if __name__ == '__main__':
    main()
