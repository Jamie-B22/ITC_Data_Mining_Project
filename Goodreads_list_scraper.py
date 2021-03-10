"""
Function for scraping a Goodreads book list page for the IDs of the books in the list

Authors: Jamie Bamforth and Jordan Ribbans
"""

import requests
import bs4
import logging
import sys

logger = logging.getLogger('List_scraper')
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

# create a file handler and add it to logger
file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def request_get(list_url, ):
    """ Takes the url for a Goodreads list and check whether the page is available for scraping
    Can take an optional proxy address as a parameter to request the page through the proxy"""
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    list_page = requests.get(list_url, headers=headers, timeout=30)
    # Next comment is to remove PyCharm warning, this broad exception is intentional.
    # noinspection PyBroadException
    try:
        list_page.raise_for_status()
    except Exception:
        logger.error(f'Failed to scrape {list_url}')
    return list_page


def list_soup(list_url):
    """ Takes a url for a Goodreads list and returns a BeautifulSoup object
    Optionally takes a proxy address to request the data through """
    list_page = request_get(list_url)

    list_page_soup = bs4.BeautifulSoup(list_page.text, 'html.parser')

    return list_page_soup


def list_parser(list_url):
    """ Takes a url for a Goodreads list, turns it into a BeautifulSoup object and returns a list of book IDs from that
    list. Books are either in a detailed list or as thumbnails, and the soup is parsed differently for each"""

    list_page_soup = list_soup(list_url)

    if "goodreads.com/book/" in list_url or "goodreads.com/list/" in list_url:  # most read and most popular list start
        # with this URL
        titles = list_page_soup.find_all("a", {"class": "bookTitle"})
        # book ID may be followed by either . or -
        book_id_list = [title['href'].split('/')[-1].split('.')[0].split('-')[0] for title in titles]
    else:
        titles = list_page_soup.find_all("div", {"class": "coverWrapper"})
        # book ID is contained at the end of the thumbnail ID, delimited by _
        book_id_list = [title['id'].rsplit('_')[-1] for title in titles]

    return book_id_list


def list_scraper(list_url):
    """
    Takes a URL for the most read, most popular or new releases lists on Goodreads and returns a list of the book IDs in
    the list .Optional parameter for a proxy address if there have been too many requests and the scraping is throttled.
    """
    logger.debug(f"Scraping list {list_url}")

    id_list = list_parser(list_url)

    return id_list


def list_scraper_tests():
    """Some tests to visually check the output is as expected. No asserts as there are external dependancies that may
    change (website may update)"""
    # print(list_scraper('http://www.goodreads.com/book/popular_by_date/2020/11', '139.99.102.114:80'))
    # print(list_scraper('https://www.goodreads.com/genres/new_releases/fiction', '139.99.102.114:80'))
    # print(list_scraper('http://www.goodreads.com/book/popular_by_date/2020/11'))
    # print(list_scraper('https://www.goodreads.com/genres/new_releases/fiction'))
    print(list_scraper('https://www.goodreads.com/list/show/158045.Thinking_with_the_Heart'))
    # print(list_scraper('https://www.goodreads.com/book/most_read?category=all&country=GB&duration=w'))


if __name__ == '__main__':
    list_scraper_tests()
