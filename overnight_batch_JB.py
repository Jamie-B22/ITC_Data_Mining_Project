from ArgParserDir.Argparser_option_functions import *

try:
    NYT_API_update_all('2020-04-01')
except Exception as err:
    logger.error(err)

try:
    NYT_API_update_all('2019-04-01')
except Exception as err:
    logger.error(err)

try:
    NYT_API_update_all('2018-04-01')
except Exception as err:
    logger.error(err)

try:
    NYT_API_update_all('2017-04-01')
except Exception as err:
    logger.error(err)

try:
    NYT_API_update_all('2016-04-01')
except Exception as err:
    logger.error(err)