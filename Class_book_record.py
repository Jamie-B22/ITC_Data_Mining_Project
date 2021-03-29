"""
Class for storing Goodreads data from book webpages.

Author: Jamie Bamforth
"""


class BookRecord:
    """
    Class for storing Goodreads data from book webpages:
        Book_ID : str - provided to the scraping function
        Title : str
        Author : str
        Format : str - e.g. hardcover, paperback, kindle
        Series : str
        Number_in_series : str
        Rating : float - range 0-5 stars
        Release_date : string format YYYY-MM-DD - for the specific edition
        First_published_date : string format YYYY-MM-DD - for the title, will be None if it is the first release
        Qty_ratings : int
        Qty_reviews : int
        Qty_pages : int
        Genres : set of str
        Scrape_datetime : string format YYYY-MM-DD hh:mm:ss
        Description : str

    Author: Jamie Bamforth
    """
    def __init__(self, data_dict):
        """Instantiate a Book_Record object by passing it a dict of the data required to set it's attribute values"""
        self.Book_ID = data_dict['Book_ID']
        self.ISBN = data_dict['ISBN']
        self.Title = data_dict['Title']
        self.Author = data_dict['Author']
        self.Format = data_dict['Format']
        self.Series = data_dict['Series']
        self.Number_in_series = data_dict['Number_in_series']
        self.Rating = data_dict['Rating']
        self.Release_date = data_dict['Release_date']
        self.First_published_date = data_dict['First_published_date']
        self.Qty_ratings = data_dict['Qty_ratings']
        self.Qty_reviews = data_dict['Qty_reviews']
        self.Qty_pages = data_dict['Qty_pages']
        self.Genres = data_dict['Genres']
        self.Scrape_datetime = data_dict['Scrape_datetime']
        self.Description = data_dict['Description'][:10000]
