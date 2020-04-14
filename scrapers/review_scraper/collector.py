import sys
import requests
import json
import time

from utilities.utils import log, get_number_of_pages
from .parser import ReviewPageParser

# example_of_full_url: 'https://www.goodreads.com/book/reviews/15797938-the-dinner?edition_reviews=true&rating=5&text_only=true&page=10'
base_url = 'https://www.goodreads.com/book/reviews/'


def collect(edition):
    '''
    Collect as many reviews as we can for edition.

    Parameters:
        edition -- An instance of Edition.
    '''
    if not edition:
        raise ValueError('edition cannot be None or empty')

    log("Collecting reviews for edition '{}'".format(edition.get_id()))

    reviews = []
    first_page_parser = get_page_parser(base_url, edition, 1)
    number_of_reviews = first_page_parser.get_number_of_text_only_reviews()

    if number_of_reviews == 300:
        log("More than 300 reviews found, collecting per rating.")
        reviews = collect_per_rating(base_url, edition)
    else:
        reviews = collect_non_top_300(first_page_parser, base_url, edition)
    return reviews


def collect_per_rating(base_url, edition):
    '''
    Collect the reviews for edition on a per rating basis.
    '''
    reviews = []
    for rating in range(1, 6):
        first_page_parser = get_page_parser(base_url, edition, 1, rating)
        number_of_reviews = first_page_parser.get_number_of_text_only_reviews()
        if number_of_reviews == 300:
            reviews.extend(collect_top_300(
                first_page_parser, base_url, edition, rating))
        else:
            reviews.extend(collect_non_top_300(
                first_page_parser, base_url, edition, rating))
    return reviews


def collect_non_top_300(first_page_parser, base_url, edition, rating=None):
    '''
    Collect all pages of reviews for a limited (i.e. not top 300) set.
    '''
    reviews = []
    number_of_reviews = first_page_parser.get_number_of_text_only_reviews()
    if first_page_parser.contains_only_reviews():
        reviews.extend(first_page_parser.get_reviews())
        number_of_pages = get_number_of_pages(number_of_reviews, 30)
        for page_number in range(2, number_of_pages + 1):
            parser = get_page_parser(base_url, edition, page_number, rating, True)
            reviews.extend(parser.get_reviews())
    else:
        if not first_page_parser.has_alternate_ratings(rating):
            reviews.extend(first_page_parser.get_reviews())
    return reviews


def collect_top_300(first_page_parser, base_url, edition, rating):
    '''
    (Naively) Collect 10 pages of 30 text_only reviews.
    '''
    reviews = first_page_parser.get_reviews()
    for page_number in range(2, 11):
        parser = get_page_parser(base_url, edition, page_number, rating)
        reviews.extend(parser.get_reviews())
    return reviews


def get_page_parser(base_url, edition, page_number, rating=None, text_only=False):
    '''
    Get an instance of ReviewPageParser with the requested page loaded.
    '''
    page_url = get_page_url(base_url, edition, page_number, rating, text_only)
    log_collection_details(edition, page_number, rating)
    html = collect_html(page_url)    
    return ReviewPageParser(html, edition)


def get_page_url(base_url, edition, page_number, rating=None, text_only=False):
    '''
    Extend base url with edition id and a query.
    Note that 'text_only=true' will always be added when page_number is 1, because
    the first page collected is used to establish how many reviews we are dealing with.

    Parameters
        text_only -- Add the 'text_only=True' query param. Defaults to False.
    '''
    url = "{}{}?edition_reviews=true".format(base_url, edition.get_id())
    if rating:
        url = "{}&rating={}".format(url, rating)
    if text_only or page_number == 1:
        url = "{}&text_only=true".format(url)
    url = "{}&page={}".format(url, page_number)
    return url


def collect_html(url):
    '''
    Do the actual request and parse the response.
    Returns a string containing the reviews as HTML (see example file).
    '''
    # response contains unicode html wrapped in some javascript
    r = requests.get(url)

    if r.status_code != 200:
        log(r.text)
        raise RuntimeError("Could not collect from url {}".format(url))

    return parse_response(r)


def parse_response(response):
    '''
    Strips some javascript surrounding the HTML, converts unicode characters, 
    replaces newlines and HTML encoded apostrophes.
    Should do the trick in most cases.
    '''
    # strip javascript
    unicode_html = response.text[26:-2]
    return json.loads(unicode_html).replace("\n", "").replace("&#39;", "'")

def log_collection_details(edition, page_number, rating=None, text_only=False):
    '''
    Log what we are collecting with some detail
    '''
    message = "  Collecting {}:".format(edition.get_id())
    if rating:
        message = "{} rating {} ^".format(message, rating)
    message = "{} page {}".format(message, page_number)
    log(message)    
