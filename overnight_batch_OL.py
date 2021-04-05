from ArgParserDir.Argparser_web_scraping import *
import logging
import sys
import time
import datetime as dt
import pymysql
from ArgParserDir.Argparser_option_functions import OL_API_update_by_author, OL_API_update_by_title

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

# create a file handler and add it to logger
file_handler = logging.FileHandler('overnight_batch_OL.log')
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

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='jordan',
                             password='password',
                             db='goodreads_data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


with connection.cursor() as cursor:
    query = "select name from authors;"
    cursor.execute(query)
    result = cursor.fetchall()
    authors = list(result)
    for author in authors:
        OL_API_update_by_author(author)


with connection.cursor() as cursor:
    query = "select title from editions;"
    cursor.execute(query)
    result = cursor.fetchall()
    titles = list(result)
    for title in titles:
        OL_API_update_by_title(title)


time_taken = round(time.time() - start_time, 2)
logger.info(f'Took {time_taken}s to run program')

