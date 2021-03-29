"""
Class for storing NYTimes bestsellers books data from NYT API.

NYT Books API user guide: https://developer.nytimes.com/docs/books-product/1/overview

Author: Jamie Bamforth
"""

import requests
import json
from config import *


class NYTimesBookList:
    """
    Class for storing getting and storing data from the NYT bestsellers lists API:
        list_name : str                 bestsellers list name
        list_name_encoded : str         bestsellers list name encoded for use in the API query string
        date : str (format YYYY-MM-DD)  date on which the list was published
        list :  list of dicts           a list of the details of the books on the bestseller list for that date


        Each book dictionary in the list consists of the following items:
            rank : integer
            rank_last_week : integer
            weeks_on_list : integer
            asterisk : integer
            dagger : integer
            primary_isbn10 : string
            primary_isbn13 : string
            publisher : string
            description : string
            price : integer
            title : string
            author : string
            contributor : string
            contributor_note : string
            book_image : string
            amazon_product_url : string
            age_group : string
            book_review_link : string
            first_chapter_link : string
            sunday_review_link : string
            article_chapter_link : string
            isbns : array object
                isbn10 : string
                isbn13 : string

    Author: Jamie Bamforth
    """
    def __init__(self, list_name_encoded, date, api_key):
        """Takes a list name and a date it was published on (accepts YYYY-MM-DD or "current") and creates a
        NYTimesBookList instance. Possible list name values can be found using static method
        NYTimesBooks.get_list_names_encoded()"""
        raw_list = self._get_list_json(list_name_encoded, date, api_key)
        self.list_name = raw_list['list_name']
        self.list_name_encoded = raw_list['list_name_encoded']
        self.date = raw_list['bestsellers_date']
        self.list = raw_list['books']

    @staticmethod
    def _get_list_json(list_name, date, api_key):
        """Takes the arguments fed into the initiation of the object and returns the 'results' key from the json
        returned by the API GET request."""
        date = '/' + date
        list_name = '/' + list_name
        url = NYT_API_BASE_URL + date + list_name + NYT_API_END_URL + api_key
        result = json.loads(requests.get(url).text)
        if result.get('status') == 'ERROR':
            raise ValueError(result['errors'][0])
        elif result.get('fault') is not None:
            raise ValueError(f"{result['fault']['detail']['errorcode']} for NYT API.")
        else:
            return result['results']

    def get_titles(self):
        """Method to return a list of the titles of the books in the NYTimesBookList instance."""
        return [book['title'] for book in self.list]

    def get_authors(self):
        """Method to return a list of the authors of the books in the NYTimesBookList instance."""
        return [book['author'] for book in self.list]

    def get_isbn10s(self):
        """Method to return a list of the ISBN 10s of the books in the NYTimesBookList instance."""
        return [book['primary_isbn10'] for book in self.list]

    def get_isbn13s(self):
        """Method to return a list of the ISBN 13s of the books in the NYTimesBookList instance."""
        return [book['primary_isbn13'] for book in self.list]

    @staticmethod
    def get_list_names(api_key):
        """Static method to return a list of all the names of all the bestseller lists."""
        url = NYT_API_BASE_URL + '/names' + NYT_API_END_URL + api_key
        list_names = json.loads(requests.get(url).text)
        return [name['list_name'] for name in list_names['results']]

    @staticmethod
    def get_list_names_encoded(api_key):
        """Static method to return a list of all the encoded names of all the bestseller lists. These encoded names can
        all be used as an input to instantiate a NYTimesBookList object"""
        url = NYT_API_BASE_URL + '/names' + NYT_API_END_URL + api_key
        list_names = json.loads(requests.get(url).text)
        return [name['list_name_encoded'] for name in list_names['results']]

    def __str__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    # some examples of outputs of static methods and class instances if this file is run standalone
    # list2 = NYTimesBookList.get_list_names_encoded(NYT_API_KEY)
    # print(len(list))
    # print(NYTimesBookList(list[0], 'current', NYT_API_KEY))
    #
    # date1 = '/current'
    # list1 = '/hardcover-fiction'
    # url = NYT_API_BASE_URL + date1 + list1 + NYT_API_END_URL + NYT_API_KEY
    # lists = json.loads(requests.get(
    #     'https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=gyAYYsc5MUxhVHVQD3AFDQznc084UhQp').text)[
    #     'results']
    #
    # list_names = json.dumps(lists, indent=3)
    # print(list_names)

    print(NYTimesBookList('hardcoverfiction', '202009', 'sjdgc'))
