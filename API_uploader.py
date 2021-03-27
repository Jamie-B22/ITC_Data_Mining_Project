from SQL_uploader import NYT_API_update_db, initialise_engine_and_base
from APIs.Class_NYTimes_List import NYTimesBookList
engine = initialise_engine_and_base()
book_list = NYTimesBookList('hardcover-fiction', 'current','gyAYYsc5MUxhVHVQD3AFDQznc084UhQp')

NYT_API_update_db(book_list, engine)