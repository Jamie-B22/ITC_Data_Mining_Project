"""
Class for storing NYTimes bestsellers books data from NYT API.

Author: Jamie Bamforth
"""

import requests
import json



NYT_API_key = 'gyAYYsc5MUxhVHVQD3AFDQznc084UhQp'
NYT_API_BASE_URL = 'https://api.nytimes.com/svc/books/v3/lists'
NYT_API_END_URL = '.json?api-key='

# class NYTimesBooks:
#
#
#
#
#     def __init__(self, API_key):
#
#@staticmethod
# def get_list_names

# date = '/current'
# list = '/hardcover-fiction'
# url = NYT_API_BASE_URL + date + list + NYT_API_END_URL + NYT_API_key
# req = requests.get(url)
# list = json.loads(req.text)
# jsontest = json.dumps(list, indent=3)
# with open('jsontest.txt', 'w') as file:
#     file.write(jsontest)
#
# for book in list['results']['books']:
#     print(book['rank'], book['title'], book['price'])

lists = json.loads(requests.get('https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=gyAYYsc5MUxhVHVQD3AFDQznc084UhQp').text)
list_names = json.dumps(lists, indent=3)
with open('NYT_list_names.txt', 'w') as file:
    file.write(list_names)
names = [name['list_name'] for name in lists['results']]
print(names)