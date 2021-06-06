
BASE_URL = "https://www.goodreads.com/"
YEAR_INDEX = 4
COUNTRY_INDEX = 2
TYPE = ""
DETAILS = ""
ANTI_THROTTLE_DELAY_S = 20
ANTI_THROTTLE_DELAY_L = 60
RELEASE_DATE_ELEMENT_ROW = 1
RELEASE_DATE_TEXT_LINE = 2
PAGES_WORD_INDEX_IN_TEXT = 0
THROTTLING_STATUS_CODE = 403
OUTPUT_FILE_NAME = "scrape_data.csv"


# Constant url root to which the unique Goodreads ID of a book is appended to access the Goodreads page for that book
ROOT_BOOK_URL = "http://www.goodreads.com/book/show/"

# For OL API
OL_BASE_URL = "https://openlibrary.org/search.json?"

# For the NYT API
NYT_API_KEY =  # Please insert your NYT API key here
NYT_API_BASE_URL = 'https://api.nytimes.com/svc/books/v3/lists'
NYT_API_END_URL = '.json?api-key='