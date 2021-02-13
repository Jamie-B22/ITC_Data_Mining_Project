"""
Function for scraping Goodreads book pages for the data:
Title
Series
Rating
Release date
Unique ID
Author
Number of ratings and reviews
Description
Date of review
Date of scraping
Number of pages
Genres (user shelves)

Extra:
Top comments
Stats table

Bonus:
Price
Status updates
World map of authors

Author: Jamie Bamforth
"""

import requests
import bs4
from datetime import datetime
import re
import time

ROOT_BOOK_URL = "https://www.goodreads.com/book/show/"


def date_from_text(date_text):
    day_pattern = re.compile(r'\b[0-9]{1,2}[a-zA-Z][a-zA-Z]\b')
    month_pattern = re.compile(
        "(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)")
    year_pattern = re.compile(r'[0-9]{4}')

    day = day_pattern.search(date_text)
    month = month_pattern.search(date_text.lower()).group().title()
    year = year_pattern.search(date_text).group()
    if day == None:
        return datetime.strptime(' '.join([month, year]), '%B %Y').strftime('%Y-%m')
    else:
        day = re.sub('[a-zA-Z]', '', day.group()) # remove suffix from day to leve number
        return datetime.strptime(' '.join([day, month, year]), '%d %B %Y').strftime('%Y-%m-%d')

def get_title(book_page_soup):
    selector = '#bookTitle'
    elems = book_page_soup.select(selector)
    return elems[0].text.strip()


def get_series(book_page_soup):
    selector = '#bookSeries > a'
    elems = book_page_soup.select(selector)
    if len(elems) == 0:
        return None
    else:
        return elems[0].text.strip().strip('()').split('#')[0].strip()


def get_num_in_series(book_page_soup):
    selector = '#bookSeries > a'
    elems = book_page_soup.select(selector)
    if len(elems) == 0:
        return None
    else:
        return float(elems[0].text.strip().strip('()').split('#')[1])


def get_author(book_page_soup):
    selector = '#bookAuthors > span:nth-child(2) > div > a > span'
    elems = book_page_soup.select(selector)
    return elems[0].text


def get_rating(book_page_soup):
    selector = '#bookMeta > span:nth-child(2)'
    elems = book_page_soup.select(selector)
    return float(elems[0].text.strip())


def get_release_date(book_page_soup):
    elems = book_page_soup.find('div', {'id': 'details'}).find_all('div')
    release_date_row = 1
    release_date_line = 2
    date_text = elems[release_date_row].text.split('\n')[release_date_line] # excludes first publised date if exists
    return date_from_text(date_text)


def get_first_published_date(book_page_soup):
    elem = book_page_soup.find('div', {'id': 'details'}).find('nobr')

    # if only on release of a book, on first published date will exist
    if elem == None:
        return None
    else:
        return date_from_text(elem.text)

def get_num_ratings(book_page_soup):
    elem = book_page_soup.find('meta', {'itemprop': 'ratingCount'})
    return int(elem['content'])


def get_num_reviews(book_page_soup):
    elem = book_page_soup.find('meta', {'itemprop': 'reviewCount'})
    return int(elem['content'])


def get_description(book_page_soup):
    selector = '#description'
    elems = book_page_soup.select(selector)
    return elems[0].text.strip().rstrip('..more').strip()


def get_num_pages(book_page_soup):
    elem = book_page_soup.find('span', {'itemprop': 'numberOfPages'})

    # some books don't have any page number info, e.g. https://www.goodreads.com/book/show/53179303-this-time-next-year-we-ll-be-laughing
    if elem == None:
        return elem
    else:
        return int(elem.text.split()[0])


def get_genre(book_page_soup):
    elems = book_page_soup.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
    genre_word_in_href = -1
    genres = {elem['href'].split('/')[genre_word_in_href] for elem in elems}  # TODO: could extract as genre > sub genre
    return genres


def book_scraper(Book_ID, proxy_address=None):
    print(f'Scraping book {Book_ID}')
    book_data = dict()
    url = ROOT_BOOK_URL + Book_ID
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
    if proxy_address == None:
        book_page = requests.get(url)
    else:
        proxies = {'http': 'http://'+proxy_address, 'https': 'https://'+proxy_address}
        book_page = requests.get(url, headers=headers, timeout=30)#, proxies=proxies, )
    try:
        book_page.raise_for_status()
    except:  # TODO: raise an error here?
        print(f'Failed to scrape {Book_ID}')

    book_page_soup = bs4.BeautifulSoup(book_page.text, 'html.parser')
    # Get data and return as correct data type
    book_data[
        'Book_ID'] = Book_ID  # keep as string for convenience of use and in case leading zeros make a difference e.g. there may be book 5598 and book 05598
    book_data['Title'] = get_title(book_page_soup)
    book_data['Author'] = get_author(book_page_soup)
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

    book_data['Description'] = get_description(book_page_soup)

    # TODO: remaining attributes:
    # Date of review
    time.sleep(10) # to avoid timeout
    return book_data


def main():
    print(book_scraper('186074'))
    print(book_scraper('72193'))
    print(book_scraper('1'))
    print(book_scraper('77203'))
    print(book_scraper('55361205'))
    print(book_scraper('53179303'))


if __name__ == '__main__':
    main()
