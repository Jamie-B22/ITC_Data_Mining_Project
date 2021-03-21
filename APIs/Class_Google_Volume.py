"""
Class for storing Google book volume data from the Google Books API.

Google books API user guide here: https://developers.google.com/books/docs/v1/using#RetrievingVolume

API key not required with GET request. However, if the call is made with authentication, each Volume will include
user-specific information, such as purchased status.

Author: Jamie Bamforth
"""

import requests
import json
from urllib.parse import quote_plus


# TODO: add exception if anything but a 200 request code is received

GGL_API_BASE_URL = 'https://www.googleapis.com/books/v1'
GGL_API_VOLUMES_SPECIFIER_URL = '/volumes?q=isbn:' # end of url accepts either an isbn10 or isbn13 to the end

# https://www.googleapis.com/books/v1/volumes?q=isbn:9781982139131

# https://www.googleapis.com/books/v1/volumes?q=intitle:life+after+death+inauthor:Sister+Souljah

class GoogleVolume:


    def __init__(self, isbn): # TODO: allow user to select whether to get book by isbn or author & title & publish date passesd as a dict
        data = self._get_volume(isbn)
        self.googleID = data['id']
        info = data['volumeInfo']
        for id in info['industryIdentifiers']:
            if id['type'] == 'ISBN_13':
                self.isbn10 = id['identifier']
            elif id['type'] == 'ISBN_10':
                self.isbn13 = id['identifier']
            else:
                pass
        self.title = info['title']
        self.subtitle = info['subtitle']
        self.authors = info['authors']
        self.first_author = info['authors'][0]
        self.published = info['publishedDate']
        self.format = info['printType']
        self.genres = info['categories']



    def _get_volume(self, isbn):
        url = GGL_API_BASE_URL + GGL_API_VOLUMES_SPECIFIER_URL + isbn
        return json.loads(requests.get(url).text)['items'][0]


    def __str__(self):
        return str(self.__dict__)





# print(quote_plus('Harry potter'))

print(GoogleVolume('9781982139131'))



