"""
Function for scraping Goodreads book pages for the data:
    Book_ID : str - provided to the scraping function
    Title : str
    Author : str
    Format : str - e.g. hardcover, paperback, kindle
    Series : str
    Number_in_series : str
    Rating : float - range 0-5 stars
    Release_date : string format YYYY-MM-DD - for the specific edition
    First_published_date : string format YYYY-MM-DD - for the title, will be None if it is the first release
    Qty_ratings : int
    Qty_reviews : int
    Qty_pages : int
    Genres : set of str
    Scrape_datetime : string format YYYY-MM-DD hh:mm:ss
    Description : str

Authors: Jamie Bamforth and Jordan Ribbans
"""

import requests
import bs4
from datetime import datetime
import re
import time
import random

# Constant url root to which the unique Goodreads ID of a book is appended to access the Goodreads page for that book
ROOT_BOOK_URL = "http://www.goodreads.com/book/show/"

ANTI_THROTTLE_DELAY_S = 10
RELEASE_DATE_ELEMENT_ROW = 1
RELEASE_DATE_TEXT_LINE = 2
PAGES_WORD_INDEX_IN_TEXT = 0
THROTTLING_STATUS_CODE = 403



def date_from_text(date_text):
    """Takes a string with the components of the date existing somewhere in the string and returns the date string in
    format YYYY-MM-DD. Date components in date_text will be in format:
        Day: number plus suffix, e.g. 1st, 5th or 22nd
        Month: full month name e.g. September
        Year: full year e.g. 1956
    If the day or day and month do not exists returns available components in format YYYY-MM or YYYY respectively."""

    # regex patterns used to find date components
    day_pattern = re.compile(r'\b[0-9]{1,2}[a-zA-Z][a-zA-Z]\b')
    month_pattern = re.compile(
        "(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)")
    year_pattern = re.compile(r'[0-9]{4}')

    # find component strings
    day = day_pattern.search(date_text)
    month = month_pattern.search(date_text.lower())
    year = year_pattern.search(date_text).group()

    # check which components exist and return correct date string
    if month == None:
        return year
    elif day == None:
        month = month.group().title()
        return datetime.strptime(' '.join([month, year]), '%B %Y').strftime('%Y-%m')
    else:
        day = re.sub('[a-zA-Z]', '', day.group())  # remove suffix from day to leve number
        month = month.group().title()
        return datetime.strptime(' '.join([day, month, year]), '%d %B %Y').strftime('%Y-%m-%d')


def get_title(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the title of the book as a string."""
    selector = '#bookTitle'
    elems = book_page_soup.select(selector)
    return elems[0].text.strip().encode('ascii', errors='ignore').decode('utf-8')


def get_format(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the format of the book as a string."""
    elem = book_page_soup.find('span', {'itemprop': 'bookFormat'})
    return elem.text.encode('ascii', errors='ignore').decode('utf-8')


def get_series(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the series the book is part of as a
    string if relevant, otherwise returns None."""
    selector = '#bookSeries > a'
    elems = book_page_soup.select(selector)
    if len(elems) == 0:
        return None
    else:
        return elems[0].text.strip().strip('()').split('#')[0].strip().encode('ascii', errors='ignore').decode('utf-8')


def get_num_in_series(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the position of the book in it's series
    as a string if relevant, otherwise returns None. Position in series is typically numeric, but may be several books
    combined into one, so returned as string to deal with edge cases (e.g. may return '1-3')."""
    selector = '#bookSeries > a'
    elems = book_page_soup.select(selector)
    if len(elems) == 0:
        return None
    else:
        return elems[0].text.strip().strip('()').split('#')[-1].encode('ascii', errors='ignore').decode('utf-8')


def get_author(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns Author as a string."""
    selector = '#bookAuthors > span:nth-child(2) > div > a > span'
    elems = book_page_soup.select(selector)
    return elems[0].text.encode('ascii', errors='ignore').decode('utf-8')


def get_rating(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns Author as a string."""
    selector = '#bookMeta > span:nth-child(2)'
    elems = book_page_soup.select(selector)
    return float(elems[0].text.strip())


def get_release_date(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns release date as a string."""
    elems = book_page_soup.find('div', {'id': 'details'}).find_all('div')
    date_text = elems[RELEASE_DATE_ELEMENT_ROW].text.split('\n')[RELEASE_DATE_TEXT_LINE]  # excludes first publised date if exists
    return date_from_text(date_text)


def get_first_published_date(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the first published date as a string.
    If this is the first edition/release of the book, will return None."""
    elem = book_page_soup.find('div', {'id': 'details'}).find('nobr')
    if elem == None:
        return None
    else:
        return date_from_text(elem.text)


def get_num_ratings(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the number of ratings on Goodreads as
    an int."""
    elem = book_page_soup.find('meta', {'itemprop': 'ratingCount'})
    return int(elem['content'])


def get_num_reviews(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the number of reviews on Goodreads as
    an int."""
    elem = book_page_soup.find('meta', {'itemprop': 'reviewCount'})
    return int(elem['content'])


def get_description(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the description on Goodreads as
    a string."""
    selector = '#description'
    elems = book_page_soup.select(selector)
    return elems[0].text.strip().rstrip('..more').strip().encode('ascii', errors='ignore').decode('utf-8')


def get_num_pages(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the number of pages as an int. If this
    information does not exist on Goodreads, returns None."""
    elem = book_page_soup.find('span', {'itemprop': 'numberOfPages'})
    if elem == None:
        return None
    else:
        return int(elem.text.split()[PAGES_WORD_INDEX_IN_TEXT])


def get_genre(book_page_soup):
    """Takes the HTML Beautiful Soup object of a Goodreads book page and returns the top genres that users have
    allocated it to on Goodreads as a set of strings."""
    elems = book_page_soup.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
    genre_word_in_href = -1
    genres = {elem['href'].split('/')[genre_word_in_href] for elem in elems}
    return genres


################# Above this line are all functions to extract the data from the Beautiful Soup object #################

def request_book_page_html(Book_ID, proxy_address):
    """Takes the Goodreads book ID and proxy address (format [IP address]:[port], or may be None) and returns a request
    object built from the Goodreads webpage for the book ID."""
    url = ROOT_BOOK_URL + Book_ID
    headers_list = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36']
    headers = {"user-agent": random.choice(headers_list)}
    book_page = requests.get(url, headers=headers)

    if book_page.status_code >= 300:
        if book_page.status_code == THROTTLING_STATUS_CODE:
            raise ConnectionError(f'Throttled by Goodreads. Failure of request to url {url}. Status code: {book_page.status_code} Error')
        else:
            raise ConnectionError(f'Failure of request to url {url}. Status code: {book_page.status_code} Error')
    return book_page


def parse_page_html(Book_ID, book_page_soup):
    """Takes the Goodreads book ID and HTML Beautiful Soup object of a Goodreads book page and retracts the relevant
    book data, returning a dictionary of the book data."""
    book_data = dict()
    book_data[
        'Book_ID'] = Book_ID  # keep as string for convenience of use and in case leading zeros make a difference e.g. there may be book 5598 and book 05598
    book_data['Title'] = get_title(book_page_soup)
    book_data['Author'] = get_author(book_page_soup)
    book_data['Format'] = get_format(book_page_soup)
    book_data['Series'] = get_series(book_page_soup)
    book_data['Number_in_series'] = get_num_in_series(book_page_soup)
    book_data['Rating'] = get_rating(book_page_soup)
    book_data['Release_date'] = get_release_date(book_page_soup)
    book_data['First_published_date'] = get_first_published_date(book_page_soup)
    book_data['Qty_ratings'] = get_num_ratings(book_page_soup)
    book_data['Qty_reviews'] = get_num_reviews(book_page_soup)
    book_data['Qty_pages'] = get_num_pages(book_page_soup)
    book_data['Genres'] = get_genre(book_page_soup)

    book_data['Scrape_datetime'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    book_data['Description'] = get_description(book_page_soup).encode('ascii', errors='ignore').decode('utf-8')
    return book_data


def book_scraper(Book_ID, proxy_address=None):
    """Takes a Goodreads book ID and an optional proxy address (format [IP address]:[port]) and returns a dictionary of
    book data scraped from the Goodreads webpage for the book ID."""
    print(f'Scraping book {Book_ID}')

    book_page = request_book_page_html(Book_ID, proxy_address)
    book_page_soup = bs4.BeautifulSoup(book_page.text, 'html.parser')
    book_data = parse_page_html(Book_ID, book_page_soup)

    time.sleep(ANTI_THROTTLE_DELAY_S + random.randint(0, 1))  # to avoid throttling, 9s wasn't enough
    return book_data


def book_scraper_tests():
    """Tests scraper against data that should not change, eg. title, author, number of pages.
    Some data such as qty reviews will change live and so is not tested."""
    # test book ID 186074
    book_data = book_scraper('186074')
    assert book_data['Book_ID'] == '186074'
    assert book_data['Title'] == 'The Name of the Wind'
    assert book_data['Author'] == 'Patrick Rothfuss'
    assert book_data['Format'] == 'Hardcover'
    assert book_data['Series'] == 'The Kingkiller Chronicle'
    assert book_data['Number_in_series'] == '1'
    assert book_data['Release_date'] == '2007-04'
    assert book_data['First_published_date'] == '2007-03-27'
    assert book_data['Qty_pages'] == 662

    # test book ID 1
    book_data = book_scraper('1')
    assert book_data['Book_ID'] == '1'
    assert book_data['Title'] == 'Harry Potter and the Half-Blood Prince'
    assert book_data['Author'] == 'J.K. Rowling'
    assert book_data['Format'] == 'Paperback'
    assert book_data['Series'] == 'Harry Potter'
    assert book_data['Number_in_series'] == '6'
    assert book_data['Release_date'] == '2006-09-16'
    assert book_data['First_published_date'] == '2005-07-16'
    assert book_data['Qty_pages'] == 652

    # test book ID 48764258
    book_data = book_scraper('48764258')
    assert book_data['Book_ID'] == '48764258'
    assert book_data['Title'] == 'Tsarina'
    assert book_data['Author'] == 'Ellen Alpsten'
    assert book_data['Format'] == 'Hardcover'
    assert book_data['Series'] == None
    assert book_data['Number_in_series'] == None
    assert book_data['Release_date'] == '2020-11-10'
    assert book_data['First_published_date'] == '2002'
    assert book_data['Qty_pages'] == 467

    print('book_scraper() tests successful')



if __name__ == '__main__':
    book_scraper_tests()
