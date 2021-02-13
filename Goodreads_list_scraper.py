"""
Function for scraping a Goodreads book list page for the IDs of the books in the list

Author: Jamie Bamforth
"""

import requests
import bs4



def list_scraper(list_url, proxy_address=None):
    print(f'Scraping list {list_url}')
    if proxy_address == None:
        list_page = requests.get(list_url)
    else:
        proxies = {'http': 'http://' + proxy_address}
        list_page = requests.get(list_url, proxies=proxies)
    try:
        list_page.raise_for_status()
    except:  # TODO: raise an error here?
        print(f'Failed to scrape {list_url}')

    list_page_soup = bs4.BeautifulSoup(list_page.text, 'html.parser')
    titles = list_page_soup.find_all("a", {"class": "bookTitle"})
    # book ID may be followed by either . or -
    book_ID_list = [title['href'].split('/')[-1].split('.')[0].split('-')[0] for title in titles]

    return book_ID_list


def main():
    print(list_scraper('https://www.goodreads.com/book/popular_by_date/2020/11', '139.99.102.114:80'))



if __name__ == '__main__':
    main()