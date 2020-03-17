import sys
import requests
import json
import time
from bs4 import BeautifulSoup

from .parser import parse_html

# example_of_full_url: 'https://www.goodreads.com/book/reviews/15797938-the-dinner?edition_reviews=true&rating=5&text_only=true&page=10'

base_url = 'https://www.goodreads.com/book/reviews/'


def collect(edition, edition_reviews=False, rating=None, text_only=False):
    '''
    Collect 10 pages of reviews given some criteria.
    Returns an array of Reviews.

    Parameters:
        edition -- The identifier of the edition as used on GoodReads (e.g. '15797938-the-dinner')
        edition_reviews -- Optional. Limit reviews to those of the provided edition. Defaults to False.
        rating -- Optional. Limit reviews to those with this rating (1 to 5). Defaults to None.
        text_only -- Optional. Limit reviews to those that include text. Defaults to False.       
    '''
    if not edition:
        raise ValueError('edition cannot be None or empty')    
    if rating and (rating < 1 or rating > 5):
        raise ValueError('rating should be a number between 1 and 5')

    url = "{}{}?edition_reviews={}".format(
        base_url, edition, 'true' if edition_reviews else 'false')    
    if rating:
        url = "{}&rating={}".format(url, rating)
    if text_only:
        url = "{}&text_only=true".format(url)

    url_no_page = url
    pages_html = []
    for i in range(1, 2):
        url = "{}&page={}".format(url_no_page, str(i))
        page_html = collect_html(url)
        pages_html.append(page_html)
        time.sleep(1)

    reviews = []

    for page in pages_html:
        reviews.extend(parse_html(page, edition))

    return reviews

def collect_html(url):
    '''
    Do the actual request and parse the response.
    Returns a string containing the reviews as HTML (see example file).
    '''
    print("collecting from '{}'".format(url))
    # response contains unicode html wrapped in some javascript
    r = requests.get(url)

    if r.status_code != 200:
        print(r.text)
        raise RuntimeError("Could not collect from url {}".format(url))
    print('collected')

    # strip javascript
    unicode_html = r.text[26:-2]
    # return clean decoded html
    return parse(unicode_html)


def parse(unicode_html):
    '''
    Convert unicode characters, replace newlines and HTML encoded apostrophes.
    Should do the trick in most cases.
    '''
    return json.loads(unicode_html).replace("\n", "").replace("&#39;", "'")


def write_to_file(file, text):
    '''
    Helper function to write text to file
    '''
    with open(file, 'w') as f:
        f.write(text)


def load_from_file(file):
    '''
    Helper function. Returns text from file.
    '''
    with open(file, 'r') as f:
        return f.read()
