
import requests
import json


BASE_URL = "https://openlibrary.org/isbn/"

isbn1 = "1250105730"
isbn2 = "198482502X"
isbnhp = "0590353403"

response = requests.get(BASE_URL + isbn2 + ".json")

ol_dict = json.loads(response.text)
# print(response.text)
print(ol_dict)
for key, value in ol_dict.items():
    print(key, ":", value)
# for key, value in response.text.items():
#     print(key, value)

## TODO: Get other books by the same author?
## TODO: Get prices from "works" page?