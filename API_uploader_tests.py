from Database.SQL_uploader import NYT_API_update_db, initialise_engine_and_base
from APIs.Class_NYTimes_List import NYTimesBookList
engine = initialise_engine_and_base()
book_list = NYTimesBookList('hardcover-fiction', 'current','gyAYYsc5MUxhVHVQD3AFDQznc084UhQp')

NYT_API_update_db(book_list, engine)

from Database.SQL_uploader import OL_API_update_db, initialise_engine_and_base
from APIs.OpenLibrary_API_Search import isbn_search, OpenLibraryBookInstance

engine = initialise_engine_and_base()
OL_book = OpenLibraryBookInstance(isbn_search("059035342X")[0])

OL_book2 = OpenLibraryBookInstance(isbn_search("9780747538486")[0])


OL_API_update_db(OL_book, engine)
OL_API_update_db(OL_book2, engine)
