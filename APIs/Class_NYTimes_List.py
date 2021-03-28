"""
Class for storing NYTimes bestsellers books data from NYT API.

NYT Books API user guide: https://developer.nytimes.com/docs/books-product/1/overview

Author: Jamie Bamforth
"""

import requests
import json

NYT_API_key = 'gyAYYsc5MUxhVHVQD3AFDQznc084UhQp'
NYT_API_BASE_URL = 'https://api.nytimes.com/svc/books/v3/lists'
NYT_API_END_URL = '.json?api-key='


class NYTimesBookList:

    def __init__(self, list_name_encoded, date, API_key):  # TODO: raise API key or date errors
        """Takes a list name and a date it was published on (accepts YYYY-MM-DD or "current") and creates a
        NYTimesBookList instance. Possible list name values can be found using static method
        NYTimesBooks.get_list_names_encoded()"""
        if list_name_encoded in self.get_list_names_encoded(API_key):
            raw_list = self._get_list_json(list_name_encoded, date, API_key)
            self.list_name = raw_list['list_name']
            self.list_name_encoded = raw_list['list_name_encoded']
            self.date = raw_list['bestsellers_date']
            self.list = raw_list['books']
        else:
            raise ValueError(
                f'Encoded list name given ({list_name_encoded}) does not exist in the NYT bestsellers list options.')

    def _get_list_json(self, list_name, date, API_key):
        date = '/' + date
        list_name = '/' + list_name
        url = NYT_API_BASE_URL + date + list_name + NYT_API_END_URL + API_key
        return json.loads(requests.get(url).text)['results']

    def get_titles(self):
        return [book['title'] for book in self.list]

    def get_authors(self):
        return [book['author'] for book in self.list]

    def get_isbn10s(self):
        return [book['primary_isbn10'] for book in self.list]

    def get_isbn13s(self):
        return [book['primary_isbn13'] for book in self.list]

    @staticmethod
    def get_list_names(API_key):
        url = NYT_API_BASE_URL + '/names' + NYT_API_END_URL + API_key
        list_names = json.loads(requests.get(url).text)
        return [name['list_name'] for name in list_names['results']]

    @staticmethod
    def get_list_names_encoded(API_key):
        url = NYT_API_BASE_URL + '/names' + NYT_API_END_URL + API_key
        list_names = json.loads(requests.get(url).text)
        return [name['list_name_encoded'] for name in list_names['results']]

    # @staticmethod
    # def get_current_list(list_name, API_key):
    #     # if list_name not in self.get_list_names(): # TODO: validate list name
    #     date = '/current'
    #     list_name = '/' + list_name.lower().replace(' ','-')
    #     url = NYT_API_BASE_URL + date + list_name + NYT_API_END_URL + API_key
    #     book_results = json.loads(requests.get(url).text)['results']['books']
    #     return book_results

    def __str__(self):
        return str(self.__dict__)


if __name__ == '__main__':
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

    # lists = json.loads(requests.get('https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=gyAYYsc5MUxhVHVQD3AFDQznc084UhQp').text)
    # list_names = json.dumps(lists, indent=3)
    # with open('NYT_list_names.txt', 'w') as file:
    #     file.write(list_names)
    # names = [name['list_name'] for name in lists['results']]
    # print(names)

    # print(NYTimesBooks.get_list_names())
    # print(NYTimesBookList.get_current_list('Hardcover Fiction', NYT_API_key))
    # print(NYTimesBookList.get_current_list('Combined Print and E-Book Fiction', NYT_API_key))
    list = NYTimesBookList.get_list_names_encoded(NYT_API_key)
    print(len(list))
    print(NYTimesBookList(list[0], 'current', NYT_API_key))

    date = '/current'
    list = '/hardcover-fiction'
    url = NYT_API_BASE_URL + date + list + NYT_API_END_URL + NYT_API_key
    lists = json.loads(requests.get('https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=gyAYYsc5MUxhVHVQD3AFDQznc084UhQp').text)['results']

    list_names = json.dumps(lists, indent=3)
    print(list_names)
    #
    # test_list = NYTimesBookList('hardcover-fiction', '2020-01-01', NYT_API_key)
    # assert test_list.list == [{'rank': 1, 'rank_last_week': 1, 'weeks_on_list': 68, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0735219095', 'primary_isbn13': '9780735219090', 'publisher': 'Putnam',
    #                            'description': 'In a quiet town on the North Carolina coast in 1969, a young woman who survived alone in the marsh becomes a murder suspect.',
    #                            'price': '0.00', 'title': 'WHERE THE CRAWDADS SING', 'author': 'Delia Owens',
    #                            'contributor': 'by Delia Owens', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780735219090.jpg',
    #                            'book_image_width': 328, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Where-Crawdads-Sing-Delia-Owens/dp/0735219095?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0735219095', 'isbn13': '9780735219090'},
    #                                      {'isbn10': '0735219117', 'isbn13': '9780735219113'},
    #                                      {'isbn10': '0525640371', 'isbn13': '9780525640370'},
    #                                      {'isbn10': '0593105419', 'isbn13': '9780593105412'},
    #                                      {'isbn10': '0593187989', 'isbn13': '9780593187982'},
    #                                      {'isbn10': '0525640363', 'isbn13': '9780525640363'},
    #                                      {'isbn10': '0735219109', 'isbn13': '9780735219106'}], 'buy_links': [
    #         {'name': 'Amazon',
    #          'url': 'https://www.amazon.com/Where-Crawdads-Sing-Delia-Owens/dp/0735219095?tag=NYTBSREV-20'},
    #         {'name': 'Apple Books',
    #          'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=WHERE+THE+CRAWDADS+SING&author=Delia+Owens'},
    #         {'name': 'Barnes and Noble',
    #          'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780735219090'},
    #         {'name': 'Books-A-Million',
    #          'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FWHERE%2BTHE%2BCRAWDADS%2BSING%2FDelia%2BOwens%2F9780735219090'},
    #         {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780735219090'},
    #         {'name': 'Indiebound', 'url': 'https://www.indiebound.org/book/9780735219090?aff=NYT'}],
    #                            'book_uri': 'nyt://book/053b4109-4555-5aa1-9b39-cc40549bcdf0'},
    #                           {'rank': 2, 'rank_last_week': 2, 'weeks_on_list': 10, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0385544189', 'primary_isbn13': '9780385544184',
    #                            'publisher': 'Doubleday',
    #                            'description': 'Cullen Post, a lawyer and Episcopal minister, antagonizes some ruthless killers when he takes on a wrongful conviction case.',
    #                            'price': '0.00', 'title': 'THE GUARDIANS', 'author': 'John Grisham',
    #                            'contributor': 'by John Grisham', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780385544184.jpg',
    #                            'book_image_width': 330, 'book_image_height': 481,
    #                            'amazon_product_url': 'https://www.amazon.com/Guardians-Novel-John-Grisham/dp/0385544189?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0385544189', 'isbn13': '9780385544184'},
    #                                      {'isbn10': '0525639365', 'isbn13': '9780525639367'},
    #                                      {'isbn10': '0385544200', 'isbn13': '9780385544207'},
    #                                      {'isbn10': '0593129989', 'isbn13': '9780593129982'},
    #                                      {'isbn10': '052562094X', 'isbn13': '9780525620945'},
    #                                      {'isbn10': '0525639381', 'isbn13': '9780525639381'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Guardians-Novel-John-Grisham/dp/0385544189?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+GUARDIANS&author=John+Grisham'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780385544184'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BGUARDIANS%2FJohn%2BGrisham%2F9780385544184'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780385544184'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780385544184?aff=NYT'}],
    #                            'book_uri': 'nyt://book/34587156-73ec-5121-946b-482b51beaf6c'},
    #                           {'rank': 3, 'rank_last_week': 4, 'weeks_on_list': 15, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '1982110562', 'primary_isbn13': '9781982110567',
    #                            'publisher': 'Scribner',
    #                            'description': 'Children with special talents are abducted and sequestered in an institution where the sinister staff seeks to extract their gifts through harsh methods.',
    #                            'price': '0.00', 'title': 'THE INSTITUTE', 'author': 'Stephen King',
    #                            'contributor': 'by Stephen King', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9781982110567.jpg',
    #                            'book_image_width': 328, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Institute-Novel-Stephen-King/dp/1982110562?tag=NYTBSREV-20',
    #                            'age_group': '',
    #                            'book_review_link': 'https://www.nytimes.com/2019/09/08/books/review-institute-stephen-king.html',
    #                            'first_chapter_link': '', 'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '1982110562', 'isbn13': '9781982110567'},
    #                                      {'isbn10': '1982110597', 'isbn13': '9781982110598'},
    #                                      {'isbn10': '1508279071', 'isbn13': '9781508279075'},
    #                                      {'isbn10': '1508279063', 'isbn13': '9781508279068'},
    #                                      {'isbn10': '1432870122', 'isbn13': '9781432870126'},
    #                                      {'isbn10': '1982110589', 'isbn13': '9781982110581'},
    #                                      {'isbn10': '1432870130', 'isbn13': '9781432870133'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Institute-Novel-Stephen-King/dp/1982110562?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+INSTITUTE&author=Stephen+King'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9781982110567'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BINSTITUTE%2FStephen%2BKing%2F9781982110567'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9781982110567'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9781982110567?aff=NYT'}],
    #                            'book_uri': 'nyt://book/ef08eed0-f900-53fe-9764-da9152bd5e8f'},
    #                           {'rank': 4, 'rank_last_week': 3, 'weeks_on_list': 4, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0316526886', 'primary_isbn13': '9780316526883',
    #                            'publisher': 'Little, Brown',
    #                            'description': 'The 27th book in the Alex Cross series. Copycat crimes make the detective question whether an innocent man was executed.',
    #                            'price': '0.00', 'title': 'CRISS CROSS', 'author': 'James Patterson',
    #                            'contributor': 'by James Patterson', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780316526883.jpg',
    #                            'book_image_width': 324, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Criss-Cross-Alex-25/dp/0316526886?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0316526886', 'isbn13': '9780316526883'},
    #                                      {'isbn10': '0316457140', 'isbn13': '9780316457149'},
    #                                      {'isbn10': '0316535648', 'isbn13': '9780316535649'},
    #                                      {'isbn10': '1538715406', 'isbn13': '9781538715406'},
    #                                      {'isbn10': '1538715392', 'isbn13': '9781538715390'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Criss-Cross-Alex-25/dp/0316526886?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=CRISS+CROSS&author=James+Patterson'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780316526883'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FCRISS%2BCROSS%2FJames%2BPatterson%2F9780316526883'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780316526883'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780316526883?aff=NYT'}],
    #                            'book_uri': 'nyt://book/47d3afff-2637-50f0-adf1-5c4a6f9dfdfd'},
    #                           {'rank': 5, 'rank_last_week': 7, 'weeks_on_list': 8, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0399593543', 'primary_isbn13': '9780399593543',
    #                            'publisher': 'Delacorte',
    #                            'description': 'Jack Reacher gets caught up in a turf war between Ukrainian and Albanian gangs.',
    #                            'price': '0.00', 'title': 'BLUE MOON', 'author': 'Lee Child',
    #                            'contributor': 'by Lee Child', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780399593543.jpg',
    #                            'book_image_width': 320, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Blue-Moon-Jack-Reacher-Novel/dp/0399593543?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0399593543', 'isbn13': '9780399593543'},
    #                                      {'isbn10': '1524774359', 'isbn13': '9781524774356'},
    #                                      {'isbn10': '1984882678', 'isbn13': '9781984882677'},
    #                                      {'isbn10': '198488266X', 'isbn13': '9781984882660'},
    #                                      {'isbn10': '039959356X', 'isbn13': '9780399593567'},
    #                                      {'isbn10': '0593129997', 'isbn13': '9780593129999'},
    #                                      {'isbn10': '0593168151', 'isbn13': '9780593168158'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Blue-Moon-Jack-Reacher-Novel/dp/0399593543?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=BLUE+MOON&author=Lee+Child'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780399593543'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FBLUE%2BMOON%2FLee%2BChild%2F9780399593543'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780399593543'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780399593543?aff=NYT'}],
    #                            'book_uri': 'nyt://book/283205a1-55a7-5e0b-89c0-a96765034edc'},
    #                           {'rank': 6, 'rank_last_week': 5, 'weeks_on_list': 5, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '1538761602', 'primary_isbn13': '9781538761601',
    #                            'publisher': 'Grand Central',
    #                            'description': 'When Atlee Pine returns to her hometown to investigate her sister’s kidnapping from 30 years ago, she winds up tracking a potential serial killer.',
    #                            'price': '0.00', 'title': 'A MINUTE TO MIDNIGHT', 'author': 'David Baldacci',
    #                            'contributor': 'by David Baldacci', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9781538761601.jpg',
    #                            'book_image_width': 328, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Minute-Midnight-Atlee-Pine-Thriller/dp/1538761602?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '1538761602', 'isbn13': '9781538761601'},
    #                                      {'isbn10': '1538734036', 'isbn13': '9781538734032'},
    #                                      {'isbn10': '1478999306', 'isbn13': '9781478999300'},
    #                                      {'isbn10': '1549120735', 'isbn13': '9781549120732'},
    #                                      {'isbn10': '1478999314', 'isbn13': '9781478999317'},
    #                                      {'isbn10': '1549120727', 'isbn13': '9781549120725'},
    #                                      {'isbn10': '1549102699', 'isbn13': '9781549102691'},
    #                                      {'isbn10': '1538761637', 'isbn13': '9781538761632'},
    #                                      {'isbn10': '1538761610', 'isbn13': '9781538761618'},
    #                                      {'isbn10': '1549104764', 'isbn13': '9781549104763'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Minute-Midnight-Atlee-Pine-Thriller/dp/1538761602?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=A+MINUTE+TO+MIDNIGHT&author=David+Baldacci'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9781538761601'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FA%2BMINUTE%2BTO%2BMIDNIGHT%2FDavid%2BBaldacci%2F9781538761601'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9781538761601'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9781538761601?aff=NYT'}],
    #                            'book_uri': 'nyt://book/a06ec543-1277-5480-bb22-f7cb9c82bf2f'},
    #                           {'rank': 7, 'rank_last_week': 6, 'weeks_on_list': 13, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0062963678', 'primary_isbn13': '9780062963673', 'publisher': 'Harper',
    #                            'description': 'A sibling relationship is impacted when the family goes from poverty to wealth and back again over the course of many decades.',
    #                            'price': '0.00', 'title': 'THE DUTCH HOUSE', 'author': 'Ann Patchett',
    #                            'contributor': 'by Ann Patchett', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780062963673.jpg',
    #                            'book_image_width': 328, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Dutch-House-Novel-Ann-Patchett/dp/0062963678?tag=NYTBSREV-20',
    #                            'age_group': '',
    #                            'book_review_link': 'https://www.nytimes.com/2019/09/21/books/review-dutch-house-ann-patchett.html',
    #                            'first_chapter_link': '', 'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0062963678', 'isbn13': '9780062963673'},
    #                                      {'isbn10': '0062963694', 'isbn13': '9780062963697'},
    #                                      {'isbn10': '0062963708', 'isbn13': '9780062963703'},
    #                                      {'isbn10': '0062963724', 'isbn13': '9780062963727'},
    #                                      {'isbn10': '0062963686', 'isbn13': '9780062963680'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Dutch-House-Novel-Ann-Patchett/dp/0062963678?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+DUTCH+HOUSE&author=Ann+Patchett'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780062963673'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BDUTCH%2BHOUSE%2FAnn%2BPatchett%2F9780062963673'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780062963673'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780062963673?aff=NYT'}],
    #                            'book_uri': 'nyt://book/0ad5db6c-4d15-5624-bef3-1385f93f78e2'},
    #                           {'rank': 8, 'rank_last_week': 8, 'weeks_on_list': 6, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0399180192', 'primary_isbn13': '9780399180194', 'publisher': 'Putnam',
    #                            'description': 'The 26th book in the Stephanie Plum series. A New Jersey gangster’s associates go after a bounty hunter’s widowed grandmother.',
    #                            'price': '0.00', 'title': 'TWISTED TWENTY-SIX', 'author': 'Janet Evanovich',
    #                            'contributor': 'by Janet Evanovich', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780399180194.jpg',
    #                            'book_image_width': 326, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Twisted-Twenty-Six-Stephanie-Janet-Evanovich/dp/0399180192?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0399180192', 'isbn13': '9780399180194'},
    #                                      {'isbn10': '0525501436', 'isbn13': '9780525501435'},
    #                                      {'isbn10': '0399180214', 'isbn13': '9780399180217'},
    #                                      {'isbn10': '0593152212', 'isbn13': '9780593152218'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Twisted-Twenty-Six-Stephanie-Janet-Evanovich/dp/0399180192?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=TWISTED+TWENTY-SIX&author=Janet+Evanovich'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780399180194'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTWISTED%2BTWENTY-SIX%2FJanet%2BEvanovich%2F9780399180194'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780399180194'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780399180194?aff=NYT'}],
    #                            'book_uri': 'nyt://book/5c932315-24db-58ed-b4ab-8313b37ab918'},
    #                           {'rank': 9, 'rank_last_week': 11, 'weeks_on_list': 29, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '1250301696', 'primary_isbn13': '9781250301697',
    #                            'publisher': 'Celadon',
    #                            'description': 'Theo Faber looks into the mystery of a famous painter who stops speaking after shooting her husband.',
    #                            'price': '0.00', 'title': 'THE SILENT PATIENT', 'author': 'Alex Michaelides',
    #                            'contributor': 'by Alex Michaelides', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9781250301697.jpg',
    #                            'book_image_width': 326, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Silent-Patient-Alex-Michaelides/dp/1250301696?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '1250301696', 'isbn13': '9781250301697'},
    #                                      {'isbn10': '1250301718', 'isbn13': '9781250301710'},
    #                                      {'isbn10': '1250317541', 'isbn13': '9781250317544'},
    #                                      {'isbn10': '1432858645', 'isbn13': '9781432858643'},
    #                                      {'isbn10': '125030170X', 'isbn13': '9781250301703'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Silent-Patient-Alex-Michaelides/dp/1250301696?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+SILENT+PATIENT&author=Alex+Michaelides'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9781250301697'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BSILENT%2BPATIENT%2FAlex%2BMichaelides%2F9781250301697'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9781250301697'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9781250301697?aff=NYT'}],
    #                            'book_uri': 'nyt://book/fe8f9863-f798-55c5-acdf-ceb32b5484ce'},
    #                           {'rank': 10, 'rank_last_week': 9, 'weeks_on_list': 14, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0385543786', 'primary_isbn13': '9780385543781',
    #                            'publisher': 'Nan A. Talese/Doubleday',
    #                            'description': 'In a sequel to “The Handmaid’s Tale,” old secrets bring three women together as the Republic of Gilead’s theocratic regime shows signs of decay.',
    #                            'price': '0.00', 'title': 'THE TESTAMENTS', 'author': 'Margaret Atwood',
    #                            'contributor': 'by Margaret Atwood', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780385543781.jpg',
    #                            'book_image_width': 326, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Testaments-Sequel-Handmaids-Tale/dp/0385543786?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0385543786', 'isbn13': '9780385543781'},
    #                                      {'isbn10': '0385543794', 'isbn13': '9780385543798'},
    #                                      {'isbn10': '0525590455', 'isbn13': '9780525590453'},
    #                                      {'isbn10': '0525562621', 'isbn13': '9780525562627'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Testaments-Sequel-Handmaids-Tale/dp/0385543786?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+TESTAMENTS&author=Margaret+Atwood'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780385543781'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BTESTAMENTS%2FMargaret%2BAtwood%2F9780385543781'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780385543781'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780385543781?aff=NYT'}],
    #                            'book_uri': 'nyt://book/e1e18717-04bb-51a2-942a-45743507535f'},
    #                           {'rank': 11, 'rank_last_week': 14, 'weeks_on_list': 12, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0399590595', 'primary_isbn13': '9780399590597',
    #                            'publisher': 'One World',
    #                            'description': 'A young man who was gifted with a mysterious power becomes part of a war between slavers and the enslaved.',
    #                            'price': '0.00', 'title': 'THE WATER DANCER', 'author': 'Ta-Nehisi Coates',
    #                            'contributor': 'by Ta-Nehisi Coates', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780399590597.jpg',
    #                            'book_image_width': 326, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Water-Dancer-Oprahs-Book-Club/dp/0399590595?tag=NYTBSREV-20',
    #                            'age_group': '',
    #                            'book_review_link': 'https://www.nytimes.com/2019/09/20/books/review-water-dancer-ta-nehisi-coates.html',
    #                            'first_chapter_link': '', 'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0399590595', 'isbn13': '9780399590597'},
    #                                      {'isbn10': '0525494847', 'isbn13': '9780525494843'},
    #                                      {'isbn10': '0399590617', 'isbn13': '9780399590610'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Water-Dancer-Oprahs-Book-Club/dp/0399590595?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+WATER+DANCER&author=Ta-Nehisi+Coates'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780399590597'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BWATER%2BDANCER%2FTa-Nehisi%2BCoates%2F9780399590597'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780399590597'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780399590597?aff=NYT'}],
    #                            'book_uri': 'nyt://book/30d61b66-0e7d-582c-a3ab-ddce005d5361'},
    #                           {'rank': 12, 'rank_last_week': 10, 'weeks_on_list': 10, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0812996542', 'primary_isbn13': '9780812996548',
    #                            'publisher': 'Random House',
    #                            'description': 'In a follow-up to the Pulitzer Prize-winning novel “Olive Kitteridge,” new relationships, including a second marriage, are encountered in a seaside town in Maine.',
    #                            'price': '0.00', 'title': 'OLIVE, AGAIN', 'author': 'Elizabeth Strout',
    #                            'contributor': 'by Elizabeth Strout', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780812996548.jpg',
    #                            'book_image_width': 327, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Olive-Again-Novel-Elizabeth-Strout/dp/0812996542?tag=NYTBSREV-20',
    #                            'age_group': '',
    #                            'book_review_link': 'https://www.nytimes.com/2019/10/15/books/review/elizabeth-strout-olive-again.html',
    #                            'first_chapter_link': '', 'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0812996542', 'isbn13': '9780812996548'},
    #                                      {'isbn10': '1643583816', 'isbn13': '9781643583815'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Olive-Again-Novel-Elizabeth-Strout/dp/0812996542?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=OLIVE%2C+AGAIN&author=Elizabeth+Strout'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780812996548'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FOLIVE%252C%2BAGAIN%2FElizabeth%2BStrout%2F9780812996548'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780812996548'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780812996548?aff=NYT'}],
    #                            'book_uri': 'nyt://book/738ec7a9-1834-5cbf-a9e0-d53d9b7dd6e0'},
    #                           {'rank': 13, 'rank_last_week': 12, 'weeks_on_list': 11, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0399562486', 'primary_isbn13': '9780399562488',
    #                            'publisher': 'Pamela Dorman/Viking',
    #                            'description': 'In Depression-era Kentucky, five women refuse to be cowed by men or convention as they deliver books.',
    #                            'price': '0.00', 'title': 'THE GIVER OF STARS', 'author': 'Jojo Moyes',
    #                            'contributor': 'by Jojo Moyes', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780399562501.jpg',
    #                            'book_image_width': 328, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Giver-Stars-Novel-Jojo-Moyes/dp/0399562486?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0399562486', 'isbn13': '9780399562488'},
    #                                      {'isbn10': '0399562508', 'isbn13': '9780399562501'},
    #                                      {'isbn10': '0525530193', 'isbn13': '9780525530190'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Giver-Stars-Novel-Jojo-Moyes/dp/0399562486?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+GIVER+OF+STARS&author=Jojo+Moyes'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780399562488'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BGIVER%2BOF%2BSTARS%2FJojo%2BMoyes%2F9780399562488'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780399562488'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780399562488?aff=NYT'}],
    #                            'book_uri': 'nyt://book/0365e66e-8090-5ec1-8d8c-2ed89027d374'},
    #                           {'rank': 14, 'rank_last_week': 15, 'weeks_on_list': 7, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '038554121X', 'primary_isbn13': '9780385541213',
    #                            'publisher': 'Doubleday',
    #                            'description': 'Zachary Ezra Rawlins fights to save a labyrinthine underground repository of stories.',
    #                            'price': '0.00', 'title': 'THE STARLESS SEA', 'author': 'Erin Morgenstern',
    #                            'contributor': 'by Erin Morgenstern', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780385541213.jpg',
    #                            'book_image_width': 326, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Starless-Sea-Novel-Erin-Morgenstern/dp/038554121X?tag=NYTBSREV-20',
    #                            'age_group': '',
    #                            'book_review_link': 'https://www.nytimes.com/2019/10/25/books/review/starless-sea-erin-morgenstern.html',
    #                            'first_chapter_link': '', 'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '038554121X', 'isbn13': '9780385541213'},
    #                                      {'isbn10': '0385541228', 'isbn13': '9780385541220'},
    #                                      {'isbn10': '0735207879', 'isbn13': '9780735207875'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Starless-Sea-Novel-Erin-Morgenstern/dp/038554121X?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=THE+STARLESS+SEA&author=Erin+Morgenstern'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780385541213'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTHE%2BSTARLESS%2BSEA%2FErin%2BMorgenstern%2F9780385541213'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780385541213'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780385541213?aff=NYT'}],
    #                            'book_uri': 'nyt://book/03931c8f-e230-5bcd-966e-5b66397ebb35'},
    #                           {'rank': 15, 'rank_last_week': 0, 'weeks_on_list': 2, 'asterisk': 0, 'dagger': 0,
    #                            'primary_isbn10': '0525541721', 'primary_isbn13': '9780525541721', 'publisher': 'Putnam',
    #                            'description': 'President Jack Ryan learns of a plot against America when he tries to help an old friend who has been arrested in Indonesia.',
    #                            'price': '0.00', 'title': 'TOM CLANCY: CODE OF HONOR', 'author': 'Marc Cameron',
    #                            'contributor': 'by Marc Cameron', 'contributor_note': '',
    #                            'book_image': 'https://storage.googleapis.com/du-prd/books/images/9780525541745.jpg',
    #                            'book_image_width': 328, 'book_image_height': 495,
    #                            'amazon_product_url': 'https://www.amazon.com/Clancy-Code-Honor-Jack-Universe-ebook/dp/B07PKJRKV7?tag=NYTBSREV-20',
    #                            'age_group': '', 'book_review_link': '', 'first_chapter_link': '',
    #                            'sunday_review_link': '', 'article_chapter_link': '',
    #                            'isbns': [{'isbn10': '0525541721', 'isbn13': '9780525541721'},
    #                                      {'isbn10': '0525541748', 'isbn13': '9780525541745'},
    #                                      {'isbn10': '052554173X', 'isbn13': '9780525541738'},
    #                                      {'isbn10': '0593152417', 'isbn13': '9780593152416'}], 'buy_links': [
    #                               {'name': 'Amazon',
    #                                'url': 'https://www.amazon.com/Clancy-Code-Honor-Jack-Universe-ebook/dp/B07PKJRKV7?tag=NYTBSREV-20'},
    #                               {'name': 'Apple Books',
    #                                'url': 'https://du-gae-books-dot-nyt-du-prd.appspot.com/buy?title=TOM+CLANCY%3A+CODE+OF+HONOR&author=Marc+Cameron'},
    #                               {'name': 'Barnes and Noble',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-11819508?url=https%3A%2F%2Fwww.barnesandnoble.com%2Fw%2F%3Fean%3D9780525541721'},
    #                               {'name': 'Books-A-Million',
    #                                'url': 'https://www.anrdoezrs.net/click-7990613-35140?url=https%3A%2F%2Fwww.booksamillion.com%2Fp%2FTOM%2BCLANCY%253A%2BCODE%2BOF%2BHONOR%2FMarc%2BCameron%2F9780525541721'},
    #                               {'name': 'Bookshop', 'url': 'https://bookshop.org/a/3546/9780525541721'},
    #                               {'name': 'Indiebound',
    #                                'url': 'https://www.indiebound.org/book/9780525541721?aff=NYT'}],
    #                            'book_uri': 'nyt://book/a44bd77d-7696-570a-80ec-8bc5946414b9'}]
    # print(test_list)
