import requests
import json

BASE_URL = "https://openlibrary.org/search.json?"


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
