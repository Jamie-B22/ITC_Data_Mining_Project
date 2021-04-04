from ArgParserDir.Argparser_web_scraping import *
import logging
import sys
import time
import datetime as dt

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

# create a file handler and add it to logger
file_handler = logging.FileHandler('overnight_batch_JR.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

start_time = time.time()
logger.info(f"Program started at {dt.datetime.now()}")

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

country_list = """
US UK IL FR BY RU BR UA CL ZA KE
"""

genres = """
Fiction
Nonfiction
Classic
Travel
Crime
"""

for year in range(2019, 2022):
    for month in range(1, 13):
        detail = str(year) + str(month).zfill(2)
        try:
            web_scraper("most-popular", detail)
        except Exception as err:
            logger.error(err)

for genre in genres.split():
    try:
        web_scraper("new-releases", genre)
    except Exception as err:
        logger.error(err)

for country in country_list.split():
    for period in ["w", "m", "y"]:
        detail = country + period
        try:
            web_scraper("most-read", detail)
        except Exception as err:
            logger.error(err)


time_taken = round(time.time() - start_time, 2)
logger.info(f'Took {time_taken}s to run program')

