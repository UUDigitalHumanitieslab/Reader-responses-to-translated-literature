import re
import requests
from urllib.parse import urlparse, urljoin

from utilities.edition import Edition
from utilities.utils import log, get_number_of_pages
from .parser import EditionPageParser

def collect(url):
    '''
    Collect all edition details from the given url.
    Returns a list of Edition instances.
    '''
    base_url = get_base_url(url)

    page1_parser = get_page_parser(base_url, 1)
    number_of_editions = page1_parser.get_number_of_editions()
    number_of_pages = get_number_of_pages(number_of_editions, 100)    
    editions = page1_parser.get_editions()

    if number_of_pages > 1:
        for page_number in range(2, number_of_pages + 1):
            parser = get_page_parser(base_url, page_number) 
            editions.extend(parser.get_editions())

    return editions


def get_page_parser(base_url, page_number):
    '''
    Get an instance of EditionPageParser with the requested page loaded.
    '''
    page_url = get_page_url(base_url, page_number)    
    log("Collecting edition details from page {}".format(page_number))
    html = collect_html(page_url)
    return EditionPageParser(html)


def collect_html(url):
    '''
    Do the actual request and parse the response.
    Returns a string containing a list of edition data as HTML (see test file for example).
    '''    
    r = requests.get(url)

    if r.status_code != 200:
        log(r.text)
        raise RuntimeError("Could not collect from url {}".format(url))
   
    return parse(r.text)

def parse(html):
    '''
    Replace newlines.
    Should do the trick in most cases.
    '''
    return html.replace("\n", "")

def get_base_url(url):
    '''
    Parse whatever url the user has provided to something without queryparameters
    '''
    parsed_url = urlparse(url)
    return urljoin(url, parsed_url.path)


def get_page_url(base_url, page_number):
    '''
    Extend page url with queryparams specifying the page number
    and the number of results per page (i.e. 100)
    '''
    return "{}?per_page=100&page={}".format(base_url, page_number)
