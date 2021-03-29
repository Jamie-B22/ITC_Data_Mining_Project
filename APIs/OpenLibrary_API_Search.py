import requests
import json
from config import OL_BASE_URL as BASE_URL


def open_library_docs_info(dictionary):
    """
    Takes a dictionary (from OpenLibrary's JSON API) and returns a list with a dictionary of important features
    for each book
    """
    book_results = []
    for i in range(len(dictionary["docs"])):
        book_data = {key: value for key, value in dictionary["docs"][i].items()
                     if key in ["title", "key", "author_name", "edition_count",
                                "publish_year", "isbn", "language", "id_goodreads", "author_key"]}
        book_results.append(book_data)
    return book_results


def author_search(author):
    """
    Takes a string as a query for a author and returns a list of dictionaries for all books that match the query
    """
    query = "author=" + author
    response = requests.get(BASE_URL + query)
    ol_dict = json.loads(response.text)
    return open_library_docs_info(ol_dict)


def isbn_search(isbn):
    """
    Takes a string as a query for an ISBN and returns a list of dictionaries for all books that match the query
    """
    query = "isbn=" + isbn
    response = requests.get(BASE_URL + query)
    ol_dict = json.loads(response.text)
    return open_library_docs_info(ol_dict)


def title_search(title):
    """
    Takes a string as a query for a book title and returns a list of dictionaries for all books that match the query
    """
    query = "title=" + title
    response = requests.get(BASE_URL + query)
    ol_dict = json.loads(response.text)
    return open_library_docs_info(ol_dict)


def all_search(search):
    """
    Takes a string as a generic query and returns a list of dictionaries for all books that match the query
    """
    query = "q=" + search
    response = requests.get(BASE_URL + query)
    ol_dict = json.loads(response.text)
    return open_library_docs_info(ol_dict)


class OpenLibraryBookInstance:
    """
    Class for storing OpenLibrary book data to a table
        OL_key : str - Unique key for each book in OpenLibrary
        Title : str
        Author : str
        Edition_count : int
        Publish_years : list of strings (which are all integers)
        ISBN : list of strings
        Languages : list of strings
        ID_goodreads : list of strings

    Author: Jordan Ribbans
    """

    def __init__(self, data_dict):
        """Instantiate a Book_Record object by passing it a dict of the data required to set it's attribute values"""
        # suffix of .encode('ascii', errors='ignore').decode('utf-8') is to fix encoding errors to UTF-8 by dropping
        # unrecognised characters
        # Openlibrary_id, Title and Author limited to 250 characters for database
        self.Openlibrary_id = data_dict.get('key').encode('ascii', errors='ignore').decode('utf-8')[:250]
        self.Title = data_dict.get('title').encode('ascii', errors='ignore').decode('utf-8')[:250]
        if data_dict.get('author_name') is not None:
            # returns the author name if the field is just a string, otherwise returns first element of list
            self.Author = (data_dict.get('author_name')[:250] if isinstance(data_dict.get('author_name'), str)
                           else data_dict.get('author_name')[0]).encode('ascii', errors='ignore').decode('utf-8')[:250]
        else:
            self.Author = None
        self.Edition_count = data_dict.get('edition_count')
        self.Publish_years = data_dict.get('publish_year')
        if data_dict.get('isbn') is not None:
            self.ISBN = [isbn.replace('-', '').encode('ascii', errors='ignore').decode('utf-8') for isbn
                         in data_dict.get('isbn')]
        else:
            self.ISBN = None
        self.Languages = data_dict.get('language')
        self.ID_goodreads = data_dict.get('id_goodreads')


def main():
    # http://openlibrary.org/search.json?author=j%20k%20rowling
    # http://openlibrary.org/search.json?isbn=059035342X

    # print(*author_search("j k rowling"), sep="\n")
    print(author_search("John Green"))
    # print(isbn_search("059035342X"))
    # for i in isbn_search("059035342X"):
    #     for key, value in i.items():
    #         print(key, ":", type(value))
    #         if isinstance(value, list):
    #             print(type(value[0]))


if __name__ == "__main__":
    main()
