"""
Functions to implement the functionality for each option the user can give to the argparser

Author: Jamie Bamforth
"""

from config import *
from APIs.Class_NYTimes_List import NYTimesBookList

def NYT_API_update_all(date):
    """Takes a date (accepts string format "YYYY-MM-DD" or "current") and fetches every NYT bestseller list for that
    date and uploads them to the database."""
    encoded_list_names = NYTimesBookList.get_list_names_encoded(NYT_API_KEY)