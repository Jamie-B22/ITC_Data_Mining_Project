"""
Function for scraping a Goodreads book list page for the IDs of the books in the list

Author: Jamie Bamforth
"""

import requests
import bs4
import time
import random




def list_scraper(list_url, proxy_address=None):
    """
    Takes a URL for the most read, most popular or new releases lists on Goodreads and returns a list of the book IDs in the list
    Optional parameter for a proxy address if there have been too many requests and the scraping is throttled
    """
    print(f'Scraping list {list_url}')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    if proxy_address == None:
        list_page = requests.get(list_url)
    else:
        proxies = {'http': proxy_address}
        list_page = requests.get(list_url, headers=headers, timeout=30)#, proxies=proxies)
    try:
        list_page.raise_for_status()
    except:  # TODO: raise an error here?
        print(f'Failed to scrape {list_url}')

    list_page_soup = bs4.BeautifulSoup(list_page.text, 'html.parser')

    # TODO: need and elif for https://www.goodreads.com/list/, e.g. https://www.goodreads.com/list/show/158045.Thinking_with_the_Heart
    if "goodreads.com/book/" in list_url:       # most read and most popular list start with this URL
        titles = list_page_soup.find_all("a", {"class": "bookTitle"})
        # book ID may be followed by either . or -
        book_ID_list = [title['href'].split('/')[-1].split('.')[0].split('-')[0] for title in titles]
    else:
        titles = list_page_soup.find_all("div", {"class": "coverWrapper"})
        # book ID is contained at the end of the thumbnail ID, delimited by _
        book_ID_list = [title['id'].rsplit('_')[-1] for title in titles]

    time.sleep(10+random.randint(0,1)) # to prevent throttling
    return book_ID_list


def main():
    print(list_scraper('http://www.goodreads.com/book/popular_by_date/2020/11', '139.99.102.114:80'))
    # print(list_scraper('https://www.goodreads.com/genres/new_releases/fiction', '139.99.102.114:80'))



if __name__ == '__main__':
    main()