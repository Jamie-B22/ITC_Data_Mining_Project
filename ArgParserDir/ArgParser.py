from ArgParserDir.Argparser_option_functions import NYT_API_update_all, NYT_API_update_list, NYT_bestesller_list_names,\
    OL_API_update_by_isbn, OL_API_update_by_author, OL_API_update_by_title
from ArgParserDir.Argparser_web_scraping import web_scraper
import argparse
import logging

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


def args_dict():
    """
    Parses arguments from command line to decide what function to run
    Uploads to database book information from GoodReads, New York Times, or Open Library
    """

    # dictionary of all the possible functions to take
    func_dict = {'most-popular': web_scraper, 'most-read': web_scraper, 'new-releases': web_scraper,
                 'custom-list': web_scraper, "NYT-API-update-all": NYT_API_update_all,
                 "NYT-API-update-list": NYT_API_update_list, "get-NYT-bestesller-list-names": NYT_bestesller_list_names,
                 "OL-author-search": OL_API_update_by_author, "OL-title-search": OL_API_update_by_title,
                 "OL-ISBN-search": OL_API_update_by_isbn}

    # first argument can be used as the key in the function dictionary
    first_arg = list(func_dict.keys())

    # second argument contains details to go into function
    second_arg = ['YYYYMM', 'COUNTRYperiod(eg ILm)', 'genre', 'customID', 'YYYY-MM-DD', 'author/title/isbn']

    # if scraping from goodreads, two arguments are needed so they are parsed differently
    scraper_arguments = ['most-popular', 'most-read', 'new-releases', 'custom-list']

    logger.debug("Parsing command line arguments")
    parser = argparse.ArgumentParser()
    parser.add_argument('type_action', choices=first_arg,
                        help=f"The type of list to scrape or action to take: {first_arg}")
    # second argument can be a long query, so we use nargs="*" to collect the remainder
    parser.add_argument('detail', help=f"The details for the corresponding list type: {second_arg}", nargs="*")

    args = parser.parse_args()

    # if the first argument says to scrape from goodreads then both arguments are needed in the func_dict function
    if args.type_action in scraper_arguments:
        logger.debug("Command line arguments parsed as scraping from GoodReads")
        func_dict[args.type_action](str(args.type_action), str(args.detail[0]))

    # otherwise we can insert the second argument into the function from func_dict
    else:
        logger.debug("Command line arguments parsed as loading information from API")
        func_dict[args.type_action](' '.join(args.detail))


def main():
    args_dict()


if __name__ == "__main__":
    main()
