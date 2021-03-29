"""
Exception subclass for enabling ScrapeErrors to be raised.

Author: Jamie Bamforth
"""


class ScrapeError(Exception):
    """Exception raised for errors encountered when scraping the html produces an unexpected output, for example due to
    a page update.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
