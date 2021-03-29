import ArgParser
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
file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def main():
    start_time = time.time()
    logger.info(f"Program started at {dt.datetime.now()}")

    ArgParser.args_dict()

    time_taken = round(time.time() - start_time, 2)
    logger.info(f'Took {time_taken}s to run program')

if __name__ == '__main__':
    main()
