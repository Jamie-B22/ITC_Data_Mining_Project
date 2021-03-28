"""
Class for storing NYTimes bestsellers books data from NYT API.

NYT Books API user guide: https://developer.nytimes.com/docs/books-product/1/overview

Author: Jamie Bamforth
"""

import requests
import json
from config import *



class NYTimesBookList:

    def __init__(self, list_name_encoded, date, API_key):  # TODO: raise API key or date errors
        """Takes a list name and a date it was published on (accepts YYYY-MM-DD or "current") and creates a
        NYTimesBookList instance. Possible list name values can be found using static method
        NYTimesBooks.get_list_names_encoded()"""
        if list_name_encoded in self.get_list_names_encoded(API_key):
            raw_list = self._get_list_json(list_name_encoded, date, API_key)
            self.list_name = raw_list['list_name']
            self.list_name_encoded = raw_list['list_name_encoded']
            self.date = raw_list['bestsellers_date']
            self.list = raw_list['books']
        else:
            raise ValueError(
                f'Encoded list name given ({list_name_encoded}) does not exist in the NYT bestsellers list options.')

    def _get_list_json(self, list_name, date, API_key):
        date = '/' + date
        list_name = '/' + list_name
        url = NYT_API_BASE_URL + date + list_name + NYT_API_END_URL + API_key
        return json.loads(requests.get(url).text)['results']

    def get_titles(self):
        return [book['title'] for book in self.list]

    def get_authors(self):
        return [book['author'] for book in self.list]

    def get_isbn10s(self):
        return [book['primary_isbn10'] for book in self.list]

    def get_isbn13s(self):
        return [book['primary_isbn13'] for book in self.list]

    @staticmethod
    def get_list_names(API_key):
        url = NYT_API_BASE_URL + '/names' + NYT_API_END_URL + API_key
        list_names = json.loads(requests.get(url).text)
        return [name['list_name'] for name in list_names['results']]

    @staticmethod
    def get_list_names_encoded(API_key):
        url = NYT_API_BASE_URL + '/names' + NYT_API_END_URL + API_key
        list_names = json.loads(requests.get(url).text)
        return [name['list_name_encoded'] for name in list_names['results']]

    # @staticmethod
    # def get_current_list(list_name, API_key):
    #     # if list_name not in self.get_list_names(): # TODO: validate list name
    #     date = '/current'
    #     list_name = '/' + list_name.lower().replace(' ','-')
    #     url = NYT_API_BASE_URL + date + list_name + NYT_API_END_URL + API_key
    #     book_results = json.loads(requests.get(url).text)['results']['books']
    #     return book_results

    def __str__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    # date = '/current'
    # list = '/hardcover-fiction'
    # url = NYT_API_BASE_URL + date + list + NYT_API_END_URL + NYT_API_key
    # req = requests.get(url)
    # list = json.loads(req.text)
    # jsontest = json.dumps(list, indent=3)
    # with open('jsontest.txt', 'w') as file:
    #     file.write(jsontest)
    #
    # for book in list['results']['books']:
    #     print(book['rank'], book['title'], book['price'])

    # lists = json.loads(requests.get('https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=gyAYYsc5MUxhVHVQD3AFDQznc084UhQp').text)
    # list_names = json.dumps(lists, indent=3)
    # with open('NYT_list_names.txt', 'w') as file:
    #     file.write(list_names)
    # names = [name['list_name'] for name in lists['results']]
    # print(names)

    # print(NYTimesBooks.get_list_names())
    # print(NYTimesBookList.get_current_list('Hardcover Fiction', NYT_API_key))
    # print(NYTimesBookList.get_current_list('Combined Print and E-Book Fiction', NYT_API_key))
    list = NYTimesBookList.get_list_names_encoded(NYT_API_KEY)
    print(len(list))
    print(NYTimesBookList(list[0], 'current', NYT_API_KEY))

    date = '/current'
    list = '/hardcover-fiction'
    url = NYT_API_BASE_URL + date + list + NYT_API_END_URL + NYT_API_KEY
    lists = json.loads(requests.get('https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=gyAYYsc5MUxhVHVQD3AFDQznc084UhQp').text)['results']

    list_names = json.dumps(lists, indent=3)
    print(list_names)
