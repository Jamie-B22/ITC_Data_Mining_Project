import requests
import json
from config import OL_BASE_URL as BASE_URL


def open_library_docs_info(dictionary):
    book_results = []
    for i in range(len(dictionary["docs"])):
        book_data = {key: value for key, value in dictionary["docs"][i].items()
                     if key in ["title", "key", "author_name", "edition_count"
                         , "publish_year", "isbn", "language", "id_goodreads", "author_key"]}
        book_results.append(book_data)
    return book_results


def author_search(author):
    query = "author=" + author
    response = requests.get(BASE_URL + query)
    ol_dict = json.loads(response.text)
    return open_library_docs_info(ol_dict)


def isbn_search(isbn):
    query = "isbn=" + isbn
    response = requests.get(BASE_URL + query)
    ol_dict = json.loads(response.text)
    return open_library_docs_info(ol_dict)


def title_search(title):
    query = "title=" + title
    response = requests.get(BASE_URL + query)
    ol_dict = json.loads(response.text)
    return open_library_docs_info(ol_dict)


def all_search(search):
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
        ISBN : list of strings (which are all integers)
        Languages : list of strings
        ID_goodreads : list of strings

    Author: Jordan Ribbans
    """
    def __init__(self, data_dict):
        """Instantiate a Book_Record object by passing it a dict of the data required to set it's attribute values"""
        self.Openlibrary_id = data_dict.get('key')
        self.Title = data_dict.get('title')
        self.Author = data_dict.get('author_name')
        self.Edition_count = data_dict.get('edition_count')
        self.Publish_years = data_dict.get('publish_year')
        self.ISBN = [isbn.replace('-','') for isbn in data_dict.get('isbn')]
        self.Languages = data_dict.get('language')
        self.ID_goodreads = data_dict.get('id_goodreads')



def main():
    # http://openlibrary.org/search.json?author=j%20k%20rowling
    # http://openlibrary.org/search.json?isbn=059035342X

    # print(*author_search("j k rowling"), sep="\n")
    # print(author_search("philomena cunk"))
    print(isbn_search("059035342X"))
    for i in isbn_search("059035342X"):
        for key, value in i.items():
            print(key, ":", type(value))
            if isinstance(value, list):
                print(type(value[0]))


if __name__ == "__main__":
    main()
