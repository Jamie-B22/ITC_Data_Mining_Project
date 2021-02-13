"""
Function for scraping a Goodreads book list page for the IDs of the books in the list

Author: Jamie Bamforth
"""

import requests
import bs4
import time



def list_scraper(list_url):
    print(f'Scraping list {list_url}')
    book_ID_list = []
    list_page = requests.get(list_url)
    try:
        list_page.raise_for_status()
    except:  # TODO: raise an error here?
        print(f'Failed to scrape {list_url}')

    list_page_soup = bs4.BeautifulSoup(list_page.text, 'html.parser')
    titles = list_page_soup.find_all("a", {"class": "bookTitle"})
    # book ID may be followed by either . or -
    book_ID_list = [title['href'].split('/')[-1].split('.')[0].split('-')[0] for title in titles]

    time.sleep(5) # to prevent throttling # TODO: really needed?
    return book_ID_list


def main():
    print(list_scraper('https://www.goodreads.com/book/popular_by_date/2020/11'))



if __name__ == '__main__':
    main()