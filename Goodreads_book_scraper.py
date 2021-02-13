"""
Function for scraping Goodreads book pages for the data:
Title
Series
Rating
Release date
Unique ID
Genre
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
import time
from datetime import datetime

ROOT_BOOK_URL = "https://www.goodreads.com/book/show/"


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


def get_release_date(book_page_soup): # TODO: use regex to extract date and also check wether it has a first published. e.g. 186074 and 55361205
    selector = '#details > div:nth-child(2) > nobr' # only when " first published..."
    # selector = '#details > div:nth-child(2)' # in all books
    elems = book_page_soup.select(selector)
    date_list = elems[0].text.strip().strip('()').split()[2:]
    day = date_list[1][:-2]
    month = date_list[0]
    year = date_list[2]
    return datetime.strptime(' '.join([day, month, year]), '%d %B %Y').strftime('%Y-%m-%d')


def get_num_ratings(book_page_soup):
    selector = '#bookMeta > a:nth-child(7)'
    elems = book_page_soup.select(selector)
    return int(elems[0].text.strip().split()[0].replace(',', ''))


def get_num_reviews(book_page_soup):
    selector = '#bookMeta > a:nth-child(9)'
    elems = book_page_soup.select(selector)
    return int(elems[0].text.strip().split()[0].replace(',', ''))


def get_description(book_page_soup):
    selector = '#description'
    elems = book_page_soup.select(selector)
    return elems[0].text.strip().rstrip('..more').strip()


def get_num_pages(book_page_soup):
    selector = '#details > div:nth-child(1) > span:last-child'
    elems = book_page_soup.select(selector)
    return int(elems[0].text.split()[0])


def get_genre(book_page_soup):
    selector = 'body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.rightContainer > div:nth-child(7) > div > div.bigBoxBody > div > div:nth-child(1) > div.left > a'
    elems = book_page_soup.select(selector)
    return elems[0].text.strip()
# body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.rightContainer > div:nth-child(6) > div > div.bigBoxBody > div > div:nth-child(1) > div.left > a
# body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.rightContainer > div:nth-child(7) > div > div.bigBoxBody > div > div:nth-child(1) > div.left > a
def book_scraper(Book_ID):
    print(f'Scraping book {Book_ID}')
    book_data = dict()
    url = ROOT_BOOK_URL + Book_ID
    book_page = requests.get(url)
    print(book_page.text[:100]) # TODO: remove, inserted to chek for throttling, throttling produces: 'This is a random-length HTML comment: hjraensvmveqvhldamygurofeqknptieddzvdcdrgoksqskglcfdiglk'
    # TODO: check if throttled and introduce a minute's wait and print 'being throttled, please wait 1 min'
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
    #book_data['Release_date'] = get_release_date(book_page_soup)
    book_data['Qty_ratings'] = get_num_ratings(book_page_soup)
    book_data['Qty_reviews'] = get_num_reviews(book_page_soup)
    book_data['Qty_pages'] = get_num_pages(book_page_soup)

    book_data['Scrape_datetime'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    book_data['Description'] = get_description(book_page_soup)
    # book_data['Genres'] = get_genre(book_page_soup)

    # TODO: remaining attributes:
    # Genre
    # Date of review
    # Genres (user shelves)

    time.sleep(5) # to prevent throttling # TODO: really needed?
    return book_data


def main():
    print(book_scraper('186074'))
    print(book_scraper('72193'))
    print(book_scraper('1'))
    print(book_scraper('77203'))
    print(book_scraper('55361205'))



if __name__ == '__main__':
    main()
